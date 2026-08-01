"""Command-line entry point for Corkaz."""

from __future__ import annotations

import sys


def main() -> None:
    """Run the interactive Corkaz chat loop."""
    from .config import Config
    from .ai import CorkAI

    config = Config()
    try:
        config.validate()
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    ai = CorkAI(config=config)

    print("Corkaz AI – type 'quit' or 'exit' to stop, 'reset' to clear history.")
    print(f"Model: {config.model}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            ai.reset()
            print("Conversation history cleared.\n")
            continue

        print("AI: ", end="", flush=True)
        try:
            for token in ai.stream_send(user_input):
                print(token, end="", flush=True)
            print()
        except Exception as exc:  # noqa: BLE001
            print(f"\nError: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
