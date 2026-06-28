import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List, Optional
from .state import AgentState
from ..rag.memory import memory_manager
from ..plugins.registry import registry
from ..core.config import settings

class PlannerOutput(BaseModel):
    intent: str = Field(description="The primary intent of the user (e.g., 'play_music', 'check_battery', 'web_search')")
    plan: List[str] = Field(description="Step-by-step plan to achieve the goal")
    plugin_name: Optional[str] = Field(description="The exact name of the plugin to use from the provided available plugins list, if any")
    plugin_params: Optional[dict] = Field(description="Parameters to pass to the plugin, matching the plugin's requirements")
    direct_response: Optional[str] = Field(description="If no plugin is needed, the direct response to the user")

def planner_node(state: AgentState):
    """
    Analyzes the user's input, detects intent, and formulates a plan using Gemini.
    """
    input_text = state.get("input_text", "").lower()
    client_id = state.get("client_id")
    
    # 1. Retrieve Context from RAG Memory
    memory_context = memory_manager.get_context(user_id=client_id, query=input_text)
    
    # 2. Get available plugins from Registry
    # Mocking React Native local plugins + Server plugins
    available_plugins = registry.get_all_configs()
    # Add known local plugins for the LLM to know about them
    available_plugins.extend([
        {"name": "BatteryPlugin", "description": "Reads device battery status and level.", "permissions": []},
        {"name": "FlashlightPlugin", "description": "Turns the device flashlight on or off. Accepts param 'action' ('on'/'off')", "permissions": ["camera"]}
    ])
    
    plugins_json = json.dumps(available_plugins, indent=2)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Planner Agent for NovaShell OS. Your job is to understand user intent and select the appropriate plugin to execute their command.\n\n"
                   "Available Plugins:\n{plugins}\n\n"
                   "User Context:\n{context}\n\n"
                   "Always return a valid JSON matching the schema."),
        ("human", "{input}")
    ])
    
    # If API key is not set, fallback to mock (for scaffolding)
    if not settings.GEMINI_API_KEY:
        if "battery" in input_text:
            return {
                "intent": "check_battery",
                "plan": ["Read battery level from device", "Format response"],
                "selected_plugin": "BatteryPlugin",
                "plugin_params": {"action": "get_status"}
            }
        elif "search" in input_text:
            return {
                "intent": "web_search",
                "plan": ["Search the web"],
                "selected_plugin": "WebSearchPlugin",
                "plugin_params": {"query": input_text.replace("search", "").strip()}
            }
        else:
            return {
                "intent": "unknown",
                "plan": ["Inform user"],
                "selected_plugin": None,
                "final_response": "I am operating in mock mode. Please set GEMINI_API_KEY in the backend config to enable active AI."
            }

    # Real LLM Invocation
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.GEMINI_API_KEY)
        structured_llm = llm.with_structured_output(PlannerOutput)
        
        chain = prompt | structured_llm
        
        result: PlannerOutput = chain.invoke({
            "plugins": plugins_json,
            "context": memory_context,
            "input": input_text
        })
        
        return {
            "intent": result.intent,
            "plan": result.plan,
            "selected_plugin": result.plugin_name,
            "plugin_params": result.plugin_params or {},
            "final_response": result.direct_response
        }
    except Exception as e:
        return {
            "intent": "error",
            "plan": ["Report error"],
            "selected_plugin": None,
            "final_response": f"AI Engine Error: {str(e)}"
        }
