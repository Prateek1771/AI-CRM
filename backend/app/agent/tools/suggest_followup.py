from pydantic import BaseModel
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from app.config import settings


class FollowUpSuggestions(BaseModel):
    suggestions: list[str]


def make_suggest_followup_tool():
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=settings.groq_api_key, temperature=0.3)

    @tool
    def suggest_followup(
        hcp_name: str,
        topics_discussed: str,
        sentiment: str,
        materials_shared: list[str] | None = None,
    ) -> dict:
        """
        Suggest 2-3 follow-up actions after logging an HCP interaction.
        Based on what was discussed and the HCP's sentiment.
        """
        structured_llm = llm.with_structured_output(FollowUpSuggestions)
        result = structured_llm.invoke(
            f"""You are a pharma sales assistant. Suggest 2-3 specific follow-up actions for a field rep
after visiting an HCP. Be concise and actionable.

HCP: {hcp_name}
Topics: {topics_discussed}
Sentiment: {sentiment}
Materials shared: {", ".join(materials_shared) if materials_shared else "none"}

Return 2-3 short follow-up action strings."""
        )
        return {"suggestions": result.suggestions}

    return suggest_followup
