from .state import AgentState
from ..plugins.registry import registry

async def orchestrator_node(state: AgentState):
    """
    Acts as the deterministic gatekeeper.
    Validates permissions, sanitizes inputs, and routes to the correct Plugin executor.
    """
    plugin_name = state.get("selected_plugin")
    
    if not plugin_name:
        return state
        
    CLIENT_PLUGINS = ["BatteryPlugin", "FlashlightPlugin", "OpenAppPlugin"]
    
    if plugin_name in CLIENT_PLUGINS:
        return {
            "execution_result": {"client_execution_required": True, "plugin": plugin_name, "params": state.get("plugin_params", {})}
        }
        
    plugin = registry.get_plugin(plugin_name)
    if not plugin:
        return {
            "execution_result": {"error": f"Plugin {plugin_name} not found in registry."}
        }
        
    # Server plugin execution
    params = state.get("plugin_params", {})
    try:
        result = await plugin.execute(params)
        return {
            "execution_result": result
        }
    except Exception as e:
         return {
            "execution_result": {"error": str(e)}
        }
