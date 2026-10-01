import json
from types import SimpleNamespace

import tools


def tool_call(name, arguments, call_id="call_1"):
    return SimpleNamespace(id=call_id, function=SimpleNamespace(name=name, arguments=arguments))


def test_record_user_details_sends_a_notification(monkeypatch):
    sent = []
    monkeypatch.setattr(tools, "push", lambda text, **kw: sent.append((text, kw)) or True)

    [result] = tools.handle_tool_calls(
        [tool_call("record_user_details", json.dumps({"email": "a@b.it", "name": "Anna"}))]
    )

    assert result["role"] == "tool" and result["tool_call_id"] == "call_1"
    assert "Anna <a@b.it>" in sent[0][0]
    assert sent[0][1]["priority"] == "high"


def test_unknown_tool_and_bad_json_do_not_crash(monkeypatch):
    monkeypatch.setattr(tools, "push", lambda *a, **k: True)
    results = tools.handle_tool_calls([
        tool_call("does_not_exist", "{}", "c1"),
        tool_call("record_unknown_question", "{not json", "c2"),
    ])
    assert "Unknown tool" in results[0]["content"]
    assert "Invalid JSON" in results[1]["content"]


def test_push_is_skipped_without_topic(monkeypatch):
    monkeypatch.setattr(tools, "NTFY_TOPIC", "")
    assert tools.push("hello") is False
