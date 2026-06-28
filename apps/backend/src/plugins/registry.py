from typing import Dict, Type
from .base import BasePlugin
from .web_search import WebSearchPlugin

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin_class: Type[BasePlugin]):
        plugin = plugin_class()
        self._plugins[plugin.config.name] = plugin
        
    def get_plugin(self, name: str) -> BasePlugin | None:
        return self._plugins.get(name)

    def get_all_configs(self) -> list[dict]:
        return [plugin.config.model_dump() for plugin in self._plugins.values()]

registry = PluginRegistry()
registry.register(WebSearchPlugin)
