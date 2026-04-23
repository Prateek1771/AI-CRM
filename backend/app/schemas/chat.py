from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    interaction_id: str | None = None
