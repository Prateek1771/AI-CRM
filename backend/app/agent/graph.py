from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from sqlalchemy.orm import Session
from app.agent.state import AgentState
from app.agent.tools.search_hcp import make_search_hcp_tool
from app.agent.tools.log_interaction import make_log_interaction_tool
from app.agent.tools.edit_interaction import make_edit_interaction_tool
from app.agent.tools.suggest_followup import make_suggest_followup_tool
from app.agent.tools.summarize_voice import make_summarize_voice_tool
from app.config import settings


def build_agent_graph(db: Session):
    tools = [
        make_search_hcp_tool(db),
        make_log_interaction_tool(db),
        make_edit_interaction_tool(db),
        make_suggest_followup_tool(),
        make_summarize_voice_tool(),
    ]

    llm = ChatGroq(
        model="gemma2-9b-it",
        api_key=settings.groq_api_key,
        temperature=0,
    ).bind_tools(tools)

    def agent_node(state: AgentState):
        response = llm.invoke(state["messages"])
        form_update = None
        if hasattr(response, "tool_calls") and response.tool_calls:
            for tc in response.tool_calls:
                if tc["name"] in ("log_interaction", "edit_interaction"):
                    pass
        return {"messages": [response], "form_update": form_update}

    def should_continue(state: AgentState):
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    def extract_form_update(state: AgentState):
        for msg in reversed(state["messages"]):
            if hasattr(msg, "content") and isinstance(msg.content, dict):
                if "form_update" in msg.content:
                    return {"form_update": msg.content["form_update"]}
        return {"form_update": None}

    tool_node = ToolNode(tools)

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue)
    graph.add_edge("tools", "agent")

    return graph.compile()
