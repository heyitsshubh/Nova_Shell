# NovaShell OS

NovaShell is an intelligent, cross-platform conversational AI operating system concept. It seamlessly connects a React Native mobile frontend (the UI shell) with a Python-based LangChain/LangGraph backend (the AI Orchestrator) to execute complex commands, control device hardware, and gather real-time data.

## Architecture

NovaShell is structured as a monorepo containing two main applications:

1. **`apps/mobile`**: The user-facing shell. Built with React Native (Expo) and styled with Tailwind CSS (NativeWind). It acts as a terminal interface for the user, executing local device plugins (like Flashlight or opening apps) and forwarding complex natural language queries to the backend.
2. **`apps/backend`**: The brain of the OS. Built with FastAPI, LangGraph, and LangChain (powered by Google's `gemini-2.5-flash`). It interprets user intents, executes remote plugins (like Web Search), and formats raw JSON data into conversational responses.

## Core Features

- **Conversational Interface**: A sleek, terminal-style UI on mobile.
- **AI Orchestration**: Uses LangGraph to plan and route user requests dynamically.
- **Local Device Plugins**:
  - `BatteryPlugin`: Reads the phone's battery level and charging status.
  - `FlashlightPlugin`: Toggles the device's camera flash on/off.
  - `OpenAppPlugin`: Deep links into installed native apps (WhatsApp, YouTube, Settings, etc.).
- **Remote Cloud Plugins**:
  - `WebSearchPlugin`: Uses DuckDuckGo to browse the live internet for up-to-date information.
- **Smart Formatting**: Raw data from plugins is fed back into the LLM to generate natural, human-like responses.

## Getting Started

To run the full NovaShell experience, you will need to start both the backend and the mobile app simultaneously.

See the specific README files for setup instructions:
- [Backend Setup Instructions](./apps/backend/README.md)
- [Mobile Setup Instructions](./apps/mobile/README.md)
