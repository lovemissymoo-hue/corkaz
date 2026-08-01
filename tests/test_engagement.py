"""Tests for corkaz.engagement."""

from __future__ import annotations

import pytest

from corkaz.engagement import EngagementRecord, EngagementStore


def test_add_and_list_records(tmp_path):
    path = tmp_path / "engagement.json"
    store = EngagementStore(str(path))
    store.add(
        EngagementRecord(
            lead="Melissa",
            activity="Community lunch",
            social_focus="Family connection",
            wellbeing_score=4,
            engagement_score=5,
            notes="Strong turnout",
        )
    )

    records = store.list()
    assert len(records) == 1
    assert records[0].lead == "Melissa"


def test_summary_per_lead(tmp_path):
    path = tmp_path / "engagement.json"
    store = EngagementStore(str(path))
    store.add(
        EngagementRecord(
            lead="Melissa",
            activity="Mentoring circle",
            social_focus="Youth confidence",
            wellbeing_score=5,
            engagement_score=4,
        )
    )
    store.add(
        EngagementRecord(
            lead="Natasha",
            activity="Sports day",
            social_focus="Social inclusion",
            wellbeing_score=4,
            engagement_score=5,
        )
    )

    melissa = store.summary(lead="Melissa")
    assert melissa["count"] == 1
    assert melissa["avg_wellbeing_score"] == 5.0
    assert melissa["avg_engagement_score"] == 4.0


def test_invalid_lead_raises():
    with pytest.raises(ValueError, match="Melissa or Natasha"):
        EngagementRecord(
            lead="Sam",  # type: ignore[arg-type]
            activity="Meeting",
            social_focus="Planning",
            wellbeing_score=3,
            engagement_score=3,
        )
