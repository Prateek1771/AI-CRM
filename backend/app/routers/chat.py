import json
from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.database import get_db
from app.schemas.chat import ChatRequest
from app.agent.graph import build_agent_graph

router = APIRouter(prefix="/api/chat", tags=["chat"])


def build_system_prompt() -> str:
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    return f"""You are an AI assistant for a pharmaceutical CRM. Your job is to help field reps log HCP (Healthcare Professional) interactions through natural conversation.

## Current date and time
Today's date: {current_date}
Current time: {current_time}

## Primary workflow

1. When a rep describes a visit, extract all information you can from their message.
2. Before calling log_interaction, you MUST have BOTH of these fields confirmed:
   - hcp_name: the name of the HCP who was visited
   - topics_discussed: what was discussed during the interaction
3. If either is missing, ask for it in a single friendly question. If both are missing, ask for both in one question.
4. Once you have hcp_name AND topics_discussed, check whether the rep mentioned a specific time or date:
   - If time WAS mentioned: call log_interaction immediately.
   - If time was NOT mentioned: ask exactly this — "The current time is {current_time} and date is {current_date} — shall I use these, or would you like to specify different ones?"
     - If the rep confirms (yes/sure/ok): call log_interaction using {current_date} as date and {current_time} as time.
     - If the rep says no or gives different values: use whatever date/time they provide, then call log_interaction.
5. After logging, always call suggest_followup.

## Tool rules
- log_interaction: only after date/time is confirmed. Pass the full conversation context as the summary.
- edit_interaction: when the rep asks to change something already logged.
- search_hcp: when the rep asks to look up an HCP.
- suggest_followup: after every successful log_interaction.
- summarize_voice: only when the rep explicitly mentions a voice note.

Be concise and professional. Ask only what is strictly necessary."""


@router.post("")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    graph = build_agent_graph(db)

    history_messages = []
    for msg in request.history:
        if msg.role == "user":
            history_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            history_messages.append(AIMessage(content=msg.content))

    initial_state = {
        "messages": [
            SystemMessage(content=build_system_prompt()),
            *history_messages,
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
