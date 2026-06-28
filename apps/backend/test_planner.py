import asyncio
from src.core.config import settings
from src.agents.planner import planner_node, AgentState

async def test():
    state = AgentState(input_text="battery", client_id="test")
    try:
        result = planner_node(state)
        print(result)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
