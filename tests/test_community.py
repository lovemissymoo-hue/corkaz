"""Tests for community lead helpers."""

from corkaz.community import build_lead_context, get_lead, list_leads


def test_list_leads_contains_melissa_and_natasha():
    leads = list_leads()
    names = {lead.name for lead in leads}
    assert names == {"Melissa", "Natasha"}


def test_get_lead_case_insensitive():
    lead = get_lead("melissa")
    assert lead is not None
    assert lead.name == "Melissa"


def test_get_lead_unknown():
    assert get_lead("unknown") is None


def test_build_lead_context_contains_core_fields():
    lead = get_lead("Natasha")
    assert lead is not None
    context = build_lead_context(lead).lower()
    assert "natasha" in context
    assert "engagement priorities" in context
    assert "social-life interests" in context
    assert "strengths" in context
