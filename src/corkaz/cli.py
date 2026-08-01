"""Command-line entry point for Corkaz."""

from __future__ import annotations

import sys


def main() -> None:
    """Run the interactive Corkaz chat loop."""
    from .config import Config
    from .ai import CorkAI
    from .engagement import EngagementRecord, EngagementStore

    config = Config()
    try:
        config.validate()
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    ai = CorkAI(config=config)
    store = EngagementStore(config.engagement_data_path)

    print("Corkaz AI – type 'quit' or 'exit' to stop, 'reset' to clear history.")
    print("Community commands:")
    print("  log Lead|Activity|Social Focus|Wellbeing(1-5)|Engagement(1-5)|Notes(optional)")
    print("  list [Melissa|Natasha]")
    print("  summary [Melissa|Natasha]")
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

        if user_input.lower().startswith("log "):
            payload = user_input[4:]
            parts = [part.strip() for part in payload.split("|")]
            if len(parts) < 5:
                print(
                    "Usage: log Lead|Activity|Social Focus|Wellbeing(1-5)|Engagement(1-5)|Notes(optional)"
                )
                continue
            notes = parts[5] if len(parts) > 5 else ""
            try:
                record = EngagementRecord(
                    lead=parts[0],
                    activity=parts[1],
                    social_focus=parts[2],
                    wellbeing_score=int(parts[3]),
                    engagement_score=int(parts[4]),
                    notes=notes,
                )
            except ValueError as exc:
                print(f"Invalid log entry: {exc}")
                continue
            store.add(record)
            print(f"Saved activity for {record.lead}.\n")
            continue

        if user_input.lower().startswith("list"):
            parts = user_input.split(maxsplit=1)
            lead = parts[1].strip() if len(parts) > 1 else None
            try:
                records = store.list(lead=lead)
            except ValueError as exc:
                print(f"Invalid list request: {exc}")
                continue
            if not records:
                print("No records found.\n")
                continue
            for idx, record in enumerate(records, start=1):
                print(
                    f"{idx}. {record.created_at} | {record.lead} | {record.activity} | "
                    f"{record.social_focus} | wellbeing {record.wellbeing_score}/5 | "
                    f"engagement {record.engagement_score}/5"
                )
                if record.notes:
                    print(f"   notes: {record.notes}")
            print()
            continue

        if user_input.lower().startswith("summary"):
            parts = user_input.split(maxsplit=1)
            lead = parts[1].strip() if len(parts) > 1 else None
            try:
                summary = store.summary(lead=lead)
            except ValueError as exc:
                print(f"Invalid summary request: {exc}")
                continue
            if summary["count"] == 0:
                print("No records found.\n")
                continue
            leads = ", ".join(summary["leads"])
            print(
                f"Records: {summary['count']}\n"
                f"Leads: {leads}\n"
                f"Average wellbeing score: {summary['avg_wellbeing_score']}\n"
                f"Average engagement score: {summary['avg_engagement_score']}\n"
            )
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
