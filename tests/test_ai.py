"""Tests for corkaz.ai (Message, ConversationHistory, CorkAI)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from corkaz.ai import ConversationHistory, CorkAI, Message
from corkaz.config import Config


# ---------------------------------------------------------------------------
# Message
# ---------------------------------------------------------------------------

class TestMessage:
    def test_valid_roles(self):
        for role in ("system", "user", "assistant"):
            m = Message(role, "hello")
            assert m.role == role
            assert m.content == "hello"

    def test_invalid_role(self):
        with pytest.raises(ValueError, match="Invalid role"):
            Message("bot", "hello")

    def test_to_dict(self):
        m = Message("user", "hi")
        assert m.to_dict() == {"role": "user", "content": "hi"}

    def test_repr(self):
        m = Message("user", "hello world")
        assert "user" in repr(m)
        assert "hello world" in repr(m)


# ---------------------------------------------------------------------------
# ConversationHistory
# ---------------------------------------------------------------------------

class TestConversationHistory:
    def test_add_and_len(self):
        h = ConversationHistory(max_history=4)
        h.add("user", "a")
        h.add("assistant", "b")
        assert len(h) == 2

    def test_eviction(self):
        h = ConversationHistory(max_history=2)
        h.add("user", "first")
        h.add("assistant", "reply")
        h.add("user", "second")   # oldest should be evicted
        assert len(h) == 2
        assert h.to_list()[0]["content"] == "reply"

    def test_clear(self):
        h = ConversationHistory()
        h.add("user", "hello")
        h.clear()
        assert len(h) == 0

    def test_to_list(self):
        h = ConversationHistory()
        h.add("user", "hello")
        lst = h.to_list()
        assert lst == [{"role": "user", "content": "hello"}]


# ---------------------------------------------------------------------------
# CorkAI (with mocked AIClient)
# ---------------------------------------------------------------------------

def _make_corkai(api_key: str = "sk-test") -> CorkAI:
    cfg = Config()
    cfg.api_key = api_key
    return CorkAI(config=cfg)


class TestCorkAI:
    def test_send_records_history(self):
        ai = _make_corkai()
        with patch.object(ai._client, "chat", return_value="Hello!"):
            reply = ai.send("Hi there")
        assert reply == "Hello!"
        assert len(ai.history) == 2  # user + assistant

    def test_reset_clears_history(self):
        ai = _make_corkai()
        with patch.object(ai._client, "chat", return_value="Hi"):
            ai.send("hello")
        assert len(ai.history) == 2
        ai.reset()
        assert len(ai.history) == 0

    def test_stream_send_assembles_reply(self):
        ai = _make_corkai()
        tokens = ["Hello", ", ", "world", "!"]
        with patch.object(ai._client, "stream", return_value=iter(tokens)):
            result = "".join(ai.stream_send("Hi"))
        assert result == "Hello, world!"
        assert len(ai.history) == 2
        assert ai.history.to_list()[-1]["content"] == "Hello, world!"

    def test_system_prompt_prepended(self):
        ai = _make_corkai()
        captured: list = []

        def fake_chat(messages):
            captured.extend(messages)
            return "ok"

        with patch.object(ai._client, "chat", side_effect=fake_chat):
            ai.send("test")

        assert captured[0]["role"] == "system"
