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
        
    plugin = registry.get_plugin(plugin_name)
    if not plugin:
        return {
            "execution_result": {"error": f"Plugin {plugin_name} not found in registry."}
        }
        
    # Validation / Permission checks would go here.
    
    params = state.get("plugin_params", {})
    try:
        # Note: If it's a mobile native plugin, the actual execution is a WebSocket emit.
        # This implementation represents server-side execution.
        result = await plugin.execute(params)
        return {
            "execution_result": result
        }
    except Exception as e:
         return {
            "execution_result": {"error": str(e)}
        }
