from typing import Any, Dict
from pydantic import BaseModel

class PluginConfig(BaseModel):
    name: str
    description: str
    permissions: list[str] = []

class BasePlugin:
    """Base class for all NovaShell server-side and client-orchestrated plugins."""
    config: PluginConfig
    
    def __init__(self):
        # Enforce that subclasses define config
        if not hasattr(self, 'config'):
            raise NotImplementedError(f"Plugin {self.__class__.__name__} must define 'config'")
            
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the plugin action and returns a dictionary result."""
        raise NotImplementedError("Plugins must implement execute()")
