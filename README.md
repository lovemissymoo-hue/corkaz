# Corkaz

A first-nation AI chat application built on top of the OpenAI API (or any compatible endpoint).

---

## Features

- Interactive streaming chat loop via the command line
- Configurable model, temperature, and conversation-history window
- Clean Python package layout ready for extension

## Requirements

- Python 3.9 or later
- An OpenAI API key (or a compatible provider)

## Installation

```bash
pip install -r requirements.txt
pip install -e .          # installs the `corkaz` CLI entry-point
```

## Quick start

```bash
export OPENAI_API_KEY="sk-..."
corkaz
```

Type your message and press **Enter**. Special commands:

| Command | Effect |
|---------|--------|
| `reset` | Clear conversation history |
| `quit` / `exit` | Exit the app |

## Configuration

All settings are read from environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | Your API key |
| `CORKAZ_MODEL` | `gpt-4o-mini` | Model to use |
| `CORKAZ_BASE_URL` | OpenAI endpoint | Override for compatible providers |
| `CORKAZ_TEMPERATURE` | `0.7` | Sampling temperature (0.0 – 2.0) |
| `CORKAZ_MAX_HISTORY` | `20` | Max messages kept in context |
| `CORKAZ_SYSTEM_PROMPT` | Built-in default | System instruction sent on every request |

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## Project layout

```
corkaz/
├── src/
│   └── corkaz/
│       ├── __init__.py   # package version
│       ├── config.py     # environment-based configuration
│       ├── ai.py         # Message, ConversationHistory, AIClient, CorkAI
│       └── cli.py        # interactive CLI entry point
├── tests/
│   ├── test_config.py
│   └── test_ai.py
├── pyproject.toml
└── requirements.txt
```

## License

MIT
