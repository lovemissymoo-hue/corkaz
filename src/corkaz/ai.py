"""Core AI chat module for Corkaz."""

from __future__ import annotations

from typing import Generator, List, Optional

from .config import Config


class Message:
    """A single chat message."""

    def __init__(self, role: str, content: str) -> None:
        if role not in ("system", "user", "assistant"):
            raise ValueError(f"Invalid role: {role!r}. Must be 'system', 'user', or 'assistant'.")
        self.role = role
        self.content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}

    def __repr__(self) -> str:
        preview = self.content[:50].replace("\n", " ")
        return f"Message(role={self.role!r}, content={preview!r})"


class ConversationHistory:
    """Manages a rolling window of conversation messages."""

    def __init__(self, max_history: int = 20) -> None:
        self._messages: List[Message] = []
        self.max_history = max_history

    def add(self, role: str, content: str) -> None:
        """Append a message and evict oldest pairs when the limit is reached."""
        self._messages.append(Message(role, content))
        # Keep at most max_history messages (evict in pairs to preserve context)
        while len(self._messages) > self.max_history:
            self._messages.pop(0)

    def clear(self) -> None:
        self._messages.clear()

    def to_list(self) -> List[dict]:
        return [m.to_dict() for m in self._messages]

    def __len__(self) -> int:
        return len(self._messages)


class AIClient:
    """Thin wrapper around the OpenAI chat-completions API."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._client = None  # Lazy-initialised in _get_client()

    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI  # type: ignore
            except ImportError as exc:
                raise ImportError(
                    "The 'openai' package is required. "
                    "Install it with: pip install openai"
                ) from exc
            self._client = OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
            )
        return self._client

    def chat(self, messages: List[dict]) -> str:
        """Send messages and return the assistant reply as a string."""
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
        )
        return response.choices[0].message.content or ""

    def stream(self, messages: List[dict]) -> Generator[str, None, None]:
        """Stream the assistant reply token by token."""
        client = self._get_client()
        stream = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content


class CorkAI:
    """High-level interface that ties together config, history, and the AI client."""

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self.history = ConversationHistory(max_history=self.config.max_history)
        self._client = AIClient(self.config)

    def _build_messages(self) -> List[dict]:
        system_msg = {"role": "system", "content": self.config.system_prompt}
        return [system_msg] + self.history.to_list()

    def send(self, user_input: str) -> str:
        """Add *user_input* to history, call the API, record the reply, and return it."""
        self.history.add("user", user_input)
        messages = self._build_messages()
        reply = self._client.chat(messages)
        self.history.add("assistant", reply)
        return reply

    def stream_send(self, user_input: str) -> Generator[str, None, None]:
        """Like *send* but yields tokens as they arrive."""
        self.history.add("user", user_input)
        messages = self._build_messages()
        full_reply: List[str] = []
        for token in self._client.stream(messages):
            full_reply.append(token)
            yield token
        self.history.add("assistant", "".join(full_reply))

    def reset(self) -> None:
        """Clear conversation history."""
        self.history.clear()
