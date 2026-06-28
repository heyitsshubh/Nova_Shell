# NovaShell Backend (AI Orchestrator)

The backend acts as the intelligent orchestrator for NovaShell. It uses LangGraph to parse user queries, decide whether a task should be handled on the server (e.g. searching the web) or the client device (e.g. turning on the flashlight), and returns formatted conversational responses.

## Tech Stack
- **Python 3.10+**
- **FastAPI**: Provides the WebSocket server to communicate with the mobile app.
- **LangChain & LangGraph**: Handles the AI agent routing, state management, and plugin execution logic.
- **Google Gemini**: Powered by `gemini-2.5-flash` for intent parsing and natural language generation.
- **DuckDuckGo**: Used for the WebSearchPlugin to fetch live internet data.

## Setup Instructions

1. **Navigate to the backend directory**:
   ```bash
   cd apps/backend
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the `apps/backend` directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_google_api_key_here
   ```

5. **Run the Server**:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## How It Works

1. The FastAPI WebSocket (`src/main.py`) receives a command from the mobile app.
2. The command is passed to the LangGraph Orchestrator (`src/agents/orchestrator.py`).
3. The **Planner Node** evaluates the command and selects an appropriate plugin.
4. If it's a *Remote Plugin* (like WebSearch), the backend executes it immediately.
5. If it's a *Client Plugin* (like Battery or Flashlight), it signals the mobile app to execute it locally.
6. The **Formatter Node** uses the LLM to translate raw JSON plugin output into a friendly response.
