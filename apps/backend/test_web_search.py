import asyncio
from src.plugins.web_search import WebSearchPlugin

async def test():
    plugin = WebSearchPlugin()
    result = await plugin.execute({"query": "latest tech news"})
    print(result)

if __name__ == "__main__":
    asyncio.run(test())
