import uuid
from datetime import datetime, date, time
from typing import Optional
from sqlalchemy import String, DateTime, Date, Time, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hcp_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("hcps.id", ondelete="SET NULL"))
    rep_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("reps.id", ondelete="SET NULL"))
    interaction_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Meeting")
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    attendees: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    topics_discussed: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    materials_shared: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    samples_distributed: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    outcomes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    follow_up_actions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    follow_up_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    raw_chat_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
