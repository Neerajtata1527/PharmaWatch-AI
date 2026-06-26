from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):

    SHIPPING_DISRUPTION = "Shipping Disruption"
    MANUFACTURING_DISRUPTION = "Manufacturing Disruption"
    TRADE_RESTRICTION = "Trade Restriction"
    GEOPOLITICAL_CONFLICT = "Geopolitical Conflict"
    NATURAL_DISASTER = "Natural Disaster"
    PUBLIC_HEALTH_EVENT = "Public Health Event"
    REGULATORY_ACTION = "Regulatory Action"
    INFRASTRUCTURE_FAILURE = "Infrastructure Failure"
    ECONOMIC_DISRUPTION = "Economic Disruption"
    OTHER = "Other"


class EventReport(BaseModel):
    """
    Structured output of the Event Intelligence Agent.
    Passed to the Research Agent.
    """

    relevant: bool

    event_type: EventType

    headline: Optional[str] = None

    summary: Optional[str] = None

    location: Optional[str] = None

    cause: Optional[str] = None

    source: Optional[str] = None

    article_url: Optional[str] = None

    published_at: Optional[str] = None

    model_config = {
        "use_enum_values": True,
    }

