from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from app.models.interaction import Interaction
from app.config import settings


class EditExtraction(BaseModel):
    field: str
    value: str | list[str] | None


def make_edit_interaction_tool(db: Session):
    llm = ChatGroq(model="gemma2-9b-it", api_key=settings.groq_api_key, temperature=0)

    @tool
    def edit_interaction(interaction_id: str, instruction: str) -> dict:
        """
        Edit a specific field of an existing interaction based on a natural language instruction.
        Example: "change sentiment to neutral" or "add Product Y to materials shared"
        """
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return {"success": False, "error": "Interaction not found"}

        structured_llm = llm.with_structured_output(EditExtraction)
        result = structured_llm.invoke(
            f"""Given this edit instruction, identify which field to change and its new value.
Fields: interaction_type, date, topics_discussed, materials_shared, samples_distributed,
sentiment (must be positive/neutral/negative), outcomes, follow_up_actions, follow_up_date.

Instruction: {instruction}"""
        )

        field = result.field
        value = result.value

        allowed_fields = {
            "interaction_type", "date", "topics_discussed", "materials_shared",
            "samples_distributed", "sentiment", "outcomes", "follow_up_actions", "follow_up_date"
        }
        if field not in allowed_fields:
            return {"success": False, "error": f"Unknown field: {field}"}

        setattr(interaction, field, value)
        db.commit()
        db.refresh(interaction)

        return {"success": True, "field": field, "value": value, "form_update": {field: value}}

    return edit_interaction
