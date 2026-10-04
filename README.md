# Digital Twin

A chatbot that answers on my behalf for anyone who wants to know about my background: experience, technical skills, projects and interests. I built it for recruiters and professional contacts who land on my profile and want to get an idea without waiting for me to reply.

Demo: https://twin-zdpe.onrender.com/ (the first visit can take about a minute: the free service goes to sleep when idle)

## How it works

The model (OpenAI, `gpt-5.4-mini` by default) gets a system prompt built from two text files:

- `summary.txt`: a short introduction of who I am, including outside of work
- `technical.txt`: a detailed professional profile with roles, technologies and projects

The prompt (`context.py`) sets strict rules. The twin says it is an AI and never pretends to be me. It does not invent experience or certifications that are not in the files, and when it does not know something it says so.

The model has two tools (function calling):

- `record_user_details`: when a visitor leaves their email to be contacted
- `record_unknown_question`: when a question comes in that the twin cannot answer

Both send a notification to my phone through [ntfy.sh](https://ntfy.sh), so I know who wants to get in touch and which information is missing from the files. When the model asks to use a tool, `app.py` runs it, sends back the result and asks again for an answer, until a text reply comes back.

Notifications are retried automatically on network errors. A tool error is returned to the model as a message, so the chat never crashes.

## Run locally

```bash
cp .env.example .env     # OPENAI_API_KEY and, if you want notifications, NTFY_TOPIC
uv venv && uv pip install -r requirements.txt
uv run app.py
```

To receive notifications, install the ntfy app and subscribe to the same topic set in `NTFY_TOPIC`. Pick a long name that is hard to guess: on the public server anyone who knows the topic can read the messages.

Tests: `uv pip install -r requirements-dev.txt`, then `pytest`.

## Files

```
app.py         Gradio interface and model call loop
context.py     system prompt, built from summary.txt and technical.txt
tools.py       model tools and ntfy notifications
styles.py      CSS, script and examples for the interface
summary.txt    personal introduction
technical.txt  professional profile
```

To adapt it to someone else, rewrite `summary.txt`, `technical.txt` and the names in `context.py`.
