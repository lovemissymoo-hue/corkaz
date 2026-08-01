"""Tests for corkaz.config."""

import os
import pytest

from corkaz.config import Config


def test_default_model():
    cfg = Config()
    assert cfg.model == "gpt-4o-mini"


def test_default_temperature():
    cfg = Config()
    assert cfg.temperature == 0.7


def test_default_max_history():
    cfg = Config()
    assert cfg.max_history == 20


def test_default_system_prompt_targets_community_engagement():
    cfg = Config()
    prompt = cfg.system_prompt.lower()
    assert "melissa" in prompt
    assert "natasha" in prompt
    assert "engagement" in prompt
    assert "social" in prompt


def test_env_override(monkeypatch):
    monkeypatch.setenv("CORKAZ_MODEL", "gpt-4o")
    monkeypatch.setenv("CORKAZ_TEMPERATURE", "1.0")
    monkeypatch.setenv("CORKAZ_MAX_HISTORY", "10")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    cfg = Config()
    assert cfg.model == "gpt-4o"
    assert cfg.temperature == 1.0
    assert cfg.max_history == 10
    assert cfg.api_key == "sk-test"


def test_validate_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    cfg = Config()
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        cfg.validate()


def test_validate_invalid_temperature(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CORKAZ_TEMPERATURE", "3.0")
    cfg = Config()
    with pytest.raises(ValueError, match="CORKAZ_TEMPERATURE"):
        cfg.validate()


def test_validate_invalid_max_history(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CORKAZ_MAX_HISTORY", "0")
    cfg = Config()
    with pytest.raises(ValueError, match="CORKAZ_MAX_HISTORY"):
        cfg.validate()


def test_validate_passes(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    cfg = Config()
    cfg.validate()  # should not raise
