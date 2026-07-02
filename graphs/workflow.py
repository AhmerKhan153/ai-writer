from langgraph.graph import END, StateGraph
from models.workflow_state import WorkflowState
from graphs.nodes import (
    approval_node,
    research_agent_node,
    topics_agent_node,
    writer_agent_node,
)

builder = StateGraph(WorkflowState)

builder.add_node("research", research_agent_node)
builder.add_node("topics", topics_agent_node)
builder.add_node("approval", approval_node)
builder.add_node("writer", writer_agent_node)


def approval_condition(state):
    return "writer" if state.get("approved") else END

builder.set_entry_point("research")
builder.add_edge("research", "topics")
builder.add_edge("topics", "approval")
builder.add_conditional_edges("approval", approval_condition)

graph = builder.compile()