import asyncio
from src.core.config import settings
from src.agents.formatter import formatter_node, AgentState

def test():
    state = AgentState(
        input_text="search the web for latest tech news",
        client_id="test",
        execution_result={'results': [{'title': "Top result for 'latest tech news'", 'snippet': 'This is a simulated search result returned by the WebSearchPlugin.'}]}
    )
    result = formatter_node(state)
    print(result)

if __name__ == "__main__":
    test()
