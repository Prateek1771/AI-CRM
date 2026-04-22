from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    interaction_id: str | None
    form_update: dict | None
    session_id: str | None
