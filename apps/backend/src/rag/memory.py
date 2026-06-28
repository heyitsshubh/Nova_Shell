from typing import List
from pydantic import BaseModel

class MemoryItem(BaseModel):
    user_id: str
    key: str
    value: str

class MemoryManager:
    def __init__(self):
        # TODO: Initialize FAISS and connect to Postgres for persistent vector storage
        self._mock_memory_store = {}

    def save_preference(self, user_id: str, key: str, value: str):
        """Saves a user preference into the memory store."""
        if user_id not in self._mock_memory_store:
            self._mock_memory_store[user_id] = {}
        self._mock_memory_store[user_id][key] = value

    def get_context(self, user_id: str, query: str) -> str:
        """
        Retrieves relevant context based on a semantic query.
        TODO: Implement embedding generation and FAISS similarity search.
        """
        user_memory = self._mock_memory_store.get(user_id, {})
        if not user_memory:
            return ""
        
        # Scaffolding: Return all known preferences
        context_parts = [f"- {k}: {v}" for k, v in user_memory.items()]
        return "User Context:\n" + "\n".join(context_parts)

memory_manager = MemoryManager()
