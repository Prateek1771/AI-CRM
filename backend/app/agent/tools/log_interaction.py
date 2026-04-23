from datetime import date as date_type, datetime
from typing import Literal
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from app.models.interaction import Interaction
from app.agent.tools.search_hcp import search_hcp_by_name
from app.config import settings


class InteractionExtraction(BaseModel):
    hcp_name: str | None = None
    interaction_type: str | None = "Meeting"
    date: str | None = None
    topics_discussed: str | None = None
    materials_shared: list[str] | None = None
    samples_distributed: list[str] | None = None
    sentiment: Literal["positive", "neutral", "negative"] | None = None
    outcomes: str | None = None
    follow_up_actions: str | None = None


def extract_interaction_fields(summary: str, llm) -> dict:
    structured_llm = llm.with_structured_output(InteractionExtraction)
    result = structured_llm.invoke(
        f"Extract HCP interaction details from this summary. Return null for fields not mentioned.\n\nSummary: {summary}"
    )
    return result.model_dump()


def make_log_interaction_tool(db: Session):
    llm = ChatGroq(model="gemma2-9b-it", api_key=settings.groq_api_key, temperature=0)

    @tool
    def log_interaction(summary: str) -> dict:
        """
        Log an HCP interaction from a natural language summary.
        Extracts all fields and saves to database.
        Returns interaction_id and form_update fields.
        """
        fields = extract_interaction_fields(summary, llm)

        hcp_id = None
        if fields.get("hcp_name"):
            hcp_result = search_hcp_by_name(fields["hcp_name"], db)
            if hcp_result["found"]:
                hcp_id = hcp_result["hcp"]["id"]

        interaction_date = date_type.today()
        if fields.get("date"):
            try:
                interaction_date = datetime.strptime(fields["date"], "%Y-%m-%d").date()
            except ValueError:
                pass

        interaction = Interaction(
            hcp_id=hcp_id,
            interaction_type=fields.get("interaction_type") or "Meeting",
            date=interaction_date,
            topics_discussed=fields.get("topics_discussed"),
            materials_shared=fields.get("materials_shared"),
            samples_distributed=fields.get("samples_distributed"),
            sentiment=fields.get("sentiment"),
            outcomes=fields.get("outcomes"),
            follow_up_actions=fields.get("follow_up_actions"),
            raw_chat_summary=summary,
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        form_update = {
            "hcp_name": fields.get("hcp_name") or "",
            "hcp_id": hcp_id,
            "interaction_type": interaction.interaction_type,
            "date": str(interaction.date),
            "topics_discussed": interaction.topics_discussed or "",
            "materials_shared": interaction.materials_shared or [],
            "samples_distributed": interaction.samples_distributed or [],
            "sentiment": interaction.sentiment,
            "outcomes": interaction.outcomes or "",
            "follow_up_actions": interaction.follow_up_actions or "",
        }

        return {"interaction_id": interaction.id, "form_update": form_update}

    return log_interaction
