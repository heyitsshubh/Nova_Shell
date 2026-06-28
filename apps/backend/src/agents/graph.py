from langgraph.graph import StateGraph, END
from .state import AgentState
from .planner import planner_node
from .orchestrator import orchestrator_node
from .formatter import formatter_node

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("formatter", formatter_node)

# Define edges
workflow.set_entry_point("planner")
workflow.add_edge("planner", "orchestrator")
workflow.add_edge("orchestrator", "formatter")
workflow.add_edge("formatter", END)

# Compile the graph
agent_graph = workflow.compile()
