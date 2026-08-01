# Corkaz

A community-led engagement and social-life app for Melissa and Natasha, with AI support built on top of the OpenAI API (or any compatible endpoint).

---

## Features

- Interactive streaming chat loop via the command line
- Built-in community activity logging for Melissa and Natasha
- Engagement and wellbeing scoring summaries
- JSON-backed local record storage
- Configurable model, temperature, and conversation-history window

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
| `log Lead\|Activity\|Social Focus\|Wellbeing\|Engagement\|Notes` | Save an engagement/social record |
| `list [Melissa\|Natasha]` | List records for one lead or both |
| `summary [Melissa\|Natasha]` | Show average wellbeing/engagement scores |

## Configuration

All settings are read from environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | Your API key |
| `CORKAZ_MODEL` | `gpt-4o-mini` | Model to use |
| `CORKAZ_BASE_URL` | OpenAI endpoint | Override for compatible providers |
| `CORKAZ_TEMPERATURE` | `0.7` | Sampling temperature (0.0 – 2.0) |
| `CORKAZ_MAX_HISTORY` | `20` | Max messages kept in context |
| `CORKAZ_SYSTEM_PROMPT` | Melissa/Natasha engagement assistant | System instruction sent on every request |
| `CORKAZ_ENGAGEMENT_DATA_PATH` | `~/.corkaz/community_engagement.json` | File path for engagement records |

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
