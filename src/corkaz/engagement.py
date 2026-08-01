"""Community lead engagement and social-life tracking."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

LeadName = Literal["Melissa", "Natasha"]
VALID_LEADS = {"Melissa", "Natasha"}


@dataclass
class EngagementRecord:
    """A single engagement/social activity record."""

    lead: LeadName
    activity: str
    social_focus: str
    wellbeing_score: int
    engagement_score: int
    notes: str = ""
    created_at: str = ""

    def __post_init__(self) -> None:
        if self.lead not in VALID_LEADS:
            raise ValueError("lead must be Melissa or Natasha")
        if not self.activity.strip():
            raise ValueError("activity is required")
        if not self.social_focus.strip():
            raise ValueError("social_focus is required")
        if not 1 <= self.wellbeing_score <= 5:
            raise ValueError("wellbeing_score must be between 1 and 5")
        if not 1 <= self.engagement_score <= 5:
            raise ValueError("engagement_score must be between 1 and 5")
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


class EngagementStore:
    """JSON-backed store for community engagement records."""

    def __init__(self, path: str) -> None:
        self.path = Path(path).expanduser()
        self._records: list[EngagementRecord] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self._records = []
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self._records = [EngagementRecord(**record) for record in raw]

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(record) for record in self._records]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(self, record: EngagementRecord) -> None:
        self._records.append(record)
        self._save()

    def list(self, lead: str | None = None) -> list[EngagementRecord]:
        if lead is None:
            return list(self._records)
        if lead not in VALID_LEADS:
            raise ValueError("lead must be Melissa or Natasha")
        return [record for record in self._records if record.lead == lead]

    def summary(self, lead: str | None = None) -> dict:
        records = self.list(lead=lead)
        if not records:
            return {
                "count": 0,
                "avg_wellbeing_score": 0.0,
                "avg_engagement_score": 0.0,
                "leads": [],
            }

        wellbeing_avg = round(
            sum(record.wellbeing_score for record in records) / len(records), 2
        )
        engagement_avg = round(
            sum(record.engagement_score for record in records) / len(records), 2
        )

        return {
            "count": len(records),
            "avg_wellbeing_score": wellbeing_avg,
            "avg_engagement_score": engagement_avg,
            "leads": sorted({record.lead for record in records}),
        }
