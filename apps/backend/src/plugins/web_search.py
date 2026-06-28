from typing import Any, Dict
from .base import BasePlugin, PluginConfig

class WebSearchPlugin(BasePlugin):
    def __init__(self):
        self.config = PluginConfig(
            name="WebSearchPlugin",
            description="Searches the web for up-to-date information.",
            permissions=["internet"]
        )

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query")
        if not query:
            return {"error": "Query parameter is required"}
            
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=3)]
                return {"results": results}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}
