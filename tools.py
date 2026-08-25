import json
import logging
import os
from typing import Literal

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("chatbot_tools")

# --- ntfy.sh configuration -------------------------------------------------
# NTFY_SERVER: use the free public server (https://ntfy.sh) or your own
#              self-hosted instance.
# NTFY_TOPIC:  a secret-ish string that acts as your "channel". Anyone who
#              knows it can read/send to it on the public server, so pick
#              something hard to guess (e.g. "marco-chatbot-9f3a2c").
# NTFY_TOKEN:  optional. Only needed if you protect your topic with access
#              tokens (recommended if you self-host or want privacy).
# NOTIFY_LANG: "it" or "en" — language used for notification titles/labels.
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")
NTFY_TOPIC = os.getenv("NTFY_TOPIC","marcoparisi-digitaltwinChatBot")
NTFY_TOKEN = os.getenv("NTFY_TOKEN")  # optional
NOTIFY_LANG = os.getenv("NOTIFY_LANG", "it").lower()

# --- simple i18n for notification titles ------------------------------------
MESSAGES = {
    "it": {
        "new_contact_title": "Nuovo contatto",
        "new_contact_fallback_name": "Nome non fornito",
        "new_contact_fallback_notes": "nessuna nota",
        "unknown_question_title": "Domanda senza risposta",
    },
    "en": {
        "new_contact_title": "New contact",
        "new_contact_fallback_name": "Name not provided",
        "new_contact_fallback_notes": "no notes",
        "unknown_question_title": "Unanswered question",
    },
}


def _t(key: str) -> str:
    """Fetch a translated label, falling back to English then the key itself."""
    lang_dict = MESSAGES.get(NOTIFY_LANG, MESSAGES["en"])
    return lang_dict.get(key, MESSAGES["en"].get(key, key))


# --- resilient HTTP session with automatic retries --------------------------
def _build_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1.0,  # 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


_session = _build_session()


def push(
    text: str,
    title: str | None = None,
    priority: Literal["min", "low", "default", "high", "urgent"] = "default",
    tags: list[str] | None = None,
) -> bool:
    """
    Send a push notification via ntfy.sh.

    Returns True if the notification was accepted by the server, False otherwise.
    Never raises: failures are logged so a notification issue never crashes
    the chatbot's tool-calling flow.
    """
    if not NTFY_TOPIC:
        logger.error("NTFY_TOPIC non impostato: impossibile inviare la notifica")
        return False

    url = f"{NTFY_SERVER}/{NTFY_TOPIC}"
    headers = {
        "Title": title or "Notifica",
        "Priority": priority,
    }
    if tags:
        headers["Tags"] = ",".join(tags)
    if NTFY_TOKEN:
        headers["Authorization"] = f"Bearer {NTFY_TOKEN}"

    try:
        response = _session.post(
            url,
            data=text.encode("utf-8"),
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        logger.info("Notifica inviata con successo: %s", title or text[:50])
        return True
    except requests.exceptions.RequestException as exc:
        logger.error("Invio notifica fallito: %s", exc)
        return False


def record_user_details(email: str, name: str | None = None, notes: str | None = None) -> str:
    name = name or _t("new_contact_fallback_name")
    notes = notes or _t("new_contact_fallback_notes")

    body = f"{name} <{email}>\n{notes}"
    push(body, title=_t("new_contact_title"), priority="high", tags=["bust_in_silhouette"])
    return "OK"


def record_unknown_question(question: str) -> str:
    push(question, title=_t("unknown_question_title"), priority="default", tags=["question"])
    return "OK"


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool = tool_map.get(tool_name)

        if tool is None:
            logger.warning("Tool sconosciuto richiesto dal modello: %s", tool_name)
            results.append(
                {
                    "role": "tool",
                    "content": json.dumps({"error": f"Unknown tool: {tool_name}"}),
                    "tool_call_id": tool_call.id,
                }
            )
            continue

        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as exc:
            logger.error("Argomenti JSON non validi per %s: %s", tool_name, exc)
            results.append(
                {
                    "role": "tool",
                    "content": json.dumps({"error": "Invalid JSON arguments"}),
                    "tool_call_id": tool_call.id,
                }
            )
            continue

        logger.info("Tool chiamato: %s con argomenti %s", tool_name, arguments)

        try:
            result = tool(**arguments)
        except Exception as exc:  # non far crashare il bot per un tool fallito
            logger.exception("Errore durante l'esecuzione di %s", tool_name)
            result = {"error": str(exc)}

        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results