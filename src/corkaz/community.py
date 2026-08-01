"""Community engagement data and prompt helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommunityLead:
    """Represents a community lead profile."""

    name: str
    role: str
    engagement_priorities: tuple[str, ...]
    social_interests: tuple[str, ...]
    strengths: tuple[str, ...]


DEFAULT_LEADS: tuple[CommunityLead, ...] = (
    CommunityLead(
        name="Melissa",
        role="Community lead for youth engagement",
        engagement_priorities=(
            "mentor young people through culture and leadership",
            "coordinate safe after-school community activities",
            "strengthen family participation in local programs",
        ),
        social_interests=(
            "group yarning circles",
            "sports and wellbeing meetups",
            "creative workshops",
        ),
        strengths=(
            "inclusive facilitation",
            "relationship building with families",
            "practical event coordination",
        ),
    ),
    CommunityLead(
        name="Natasha",
        role="Community lead for women and intergenerational connection",
        engagement_priorities=(
            "support women-led initiatives",
            "connect Elders and young adults through shared learning",
            "build partnerships with local services",
        ),
        social_interests=(
            "community cooking and food sharing",
            "arts, language and storytelling sessions",
            "social support gatherings",
        ),
        strengths=(
            "cross-generation relationship building",
            "program design with cultural grounding",
            "stakeholder collaboration",
        ),
    ),
)


def list_leads() -> tuple[CommunityLead, ...]:
    """Return all known community leads."""
    return DEFAULT_LEADS


def get_lead(name: str) -> CommunityLead | None:
    """Return a lead by case-insensitive name."""
    normalized = name.strip().lower()
    for lead in DEFAULT_LEADS:
        if lead.name.lower() == normalized:
            return lead
    return None


def build_lead_context(lead: CommunityLead) -> str:
    """Build contextual text for prompt injection."""
    priorities = "; ".join(lead.engagement_priorities)
    social = "; ".join(lead.social_interests)
    strengths = "; ".join(lead.strengths)
    return (
        f"Focus person: {lead.name}. "
        f"Role: {lead.role}. "
        f"Engagement priorities: {priorities}. "
        f"Social-life interests: {social}. "
        f"Key strengths: {strengths}. "
        "Give practical, culturally respectful, community-first guidance."
    )
