from pydantic import BaseModel
from datetime import datetime
from datetime import date as DateType
from datetime import time as TimeType
from typing import Literal


class InteractionCreate(BaseModel):
    hcp_id: str | None = None
    rep_id: str | None = None
    interaction_type: str = "Meeting"
    date: DateType
    time: TimeType | None = None
    attendees: list[str] | None = None
    topics_discussed: str | None = None
    materials_shared: list[str] | None = None
    samples_distributed: list[str] | None = None
    sentiment: Literal["positive", "neutral", "negative"] | None = None
    outcomes: str | None = None
    follow_up_actions: str | None = None
    follow_up_date: DateType | None = None
    raw_chat_summary: str | None = None


class InteractionUpdate(BaseModel):
    interaction_type: str | None = None
    date: DateType | None = None
    time: TimeType | None = None
    attendees: list[str] | None = None
    topics_discussed: str | None = None
    materials_shared: list[str] | None = None
    samples_distributed: list[str] | None = None
    sentiment: Literal["positive", "neutral", "negative"] | None = None
    outcomes: str | None = None
    follow_up_actions: str | None = None
    follow_up_date: DateType | None = None


class InteractionRead(InteractionCreate):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
