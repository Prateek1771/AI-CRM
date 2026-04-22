import uuid
from datetime import datetime, date, time
from sqlalchemy import String, DateTime, Date, Time, Text, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    hcp_id: Mapped[str | None] = mapped_column(String, ForeignKey("hcps.id", ondelete="SET NULL"))
    rep_id: Mapped[str | None] = mapped_column(String, ForeignKey("reps.id", ondelete="SET NULL"))
    interaction_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Meeting")
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time | None] = mapped_column(Time)
    attendees: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    topics_discussed: Mapped[str | None] = mapped_column(Text)
    materials_shared: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    samples_distributed: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    sentiment: Mapped[str | None] = mapped_column(String(20))
    outcomes: Mapped[str | None] = mapped_column(Text)
    follow_up_actions: Mapped[str | None] = mapped_column(Text)
    follow_up_date: Mapped[date | None] = mapped_column(Date)
    raw_chat_summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
