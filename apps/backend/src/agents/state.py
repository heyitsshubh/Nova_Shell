from typing import TypedDict, List, Optional, Any
from pydantic import BaseModel

class AgentState(TypedDict):
    input_text: str
    client_id: str
    intent: Optional[str]
    plan: Optional[List[str]]
    selected_plugin: Optional[str]
    plugin_params: Optional[dict]
    execution_result: Optional[Any]
    final_response: Optional[str]
