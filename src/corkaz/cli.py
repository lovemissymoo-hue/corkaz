"""Command-line entry point for Corkaz."""

from __future__ import annotations

import sys

from .community import build_lead_context, get_lead, list_leads


def _print_help() -> None:
    print(
        "Commands:\n"
        "  leads                         List available community leads\n"
        "  lead <name>                   Show lead profile\n"
        "  engage <name> <topic>         Generate engagement guidance\n"
        "  social <name>                 Generate social life support ideas\n"
        "  reset                         Clear conversation history\n"
        "  quit / exit                   Exit the app\n"
    )


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

    print("Corkaz AI – Melissa and Natasha community engagement assistant.")
    print("Type 'help' for commands.")
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

        if user_input.lower() == "help":
            _print_help()
            continue

        if user_input.lower() == "leads":
            print("Community leads:")
            for lead in list_leads():
                print(f"- {lead.name}: {lead.role}")
            print()
            continue

        if user_input.lower().startswith("lead "):
            _, _, name = user_input.partition(" ")
            lead = get_lead(name)
            if lead is None:
                print("Lead not found. Try: Melissa or Natasha.\n")
                continue
            print(f"{lead.name} ({lead.role})")
            print("Engagement priorities:")
            for item in lead.engagement_priorities:
                print(f"- {item}")
            print("Social interests:")
            for item in lead.social_interests:
                print(f"- {item}")
            print("Strengths:")
            for item in lead.strengths:
                print(f"- {item}")
            print()
            continue

        if user_input.lower().startswith("engage "):
            _, _, tail = user_input.partition(" ")
            name, _, topic = tail.partition(" ")
            lead = get_lead(name)
            if lead is None or not topic.strip():
                print("Usage: engage <Melissa|Natasha> <topic>\n")
                continue
            user_input = (
                f"{build_lead_context(lead)} "
                f"Create a community-lead engagement action plan for topic: {topic.strip()}."
            )

        elif user_input.lower().startswith("social "):
            _, _, name = user_input.partition(" ")
            lead = get_lead(name)
            if lead is None:
                print("Usage: social <Melissa|Natasha>\n")
                continue
            user_input = (
                f"{build_lead_context(lead)} "
                "Create a weekly social-life support plan with inclusive activities, wellbeing steps, "
                "and culturally grounded community connections."
            )

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
