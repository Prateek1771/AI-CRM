import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage
from app.database import get_db
from app.schemas.chat import ChatRequest
from app.agent.graph import build_agent_graph

router = APIRouter(prefix="/api/chat", tags=["chat"])

SYSTEM_PROMPT = """You are an AI assistant for a pharmaceutical CRM. Help field reps log HCP interactions.

When a rep describes a visit, use the log_interaction tool to extract and save the interaction.
When asked to edit something, use the edit_interaction tool.
When looking up an HCP, use the search_hcp tool.
After logging, always use suggest_followup to offer next steps.

Be concise and professional."""


@router.post("")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    graph = build_agent_graph(db)

    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=request.message),
        ],
        "interaction_id": request.interaction_id,
        "form_update": None,
        "session_id": request.session_id,
    }

    async def event_stream():
        final_state = graph.invoke(initial_state)

        ai_messages = [
            m for m in final_state["messages"]
            if hasattr(m, "type") and m.type == "ai" and not getattr(m, "tool_calls", None)
        ]

        response_text = ai_messages[-1].content if ai_messages else "Done."

        # Extract form_update from tool results (log_interaction / edit_interaction return it)
        form_update = None
        for msg in final_state["messages"]:
            if getattr(msg, "type", None) == "tool":
                try:
                    content = msg.content
                    tool_result = json.loads(content) if isinstance(content, str) else content
                    if isinstance(tool_result, dict) and "form_update" in tool_result:
                        form_update = tool_result["form_update"]
                except (json.JSONDecodeError, TypeError):
                    pass

        for chunk in response_text:
            yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"

        if form_update:
            yield f"data: {json.dumps({'type': 'form_update', 'fields': form_update})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
