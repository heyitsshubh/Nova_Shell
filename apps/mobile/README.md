# NovaShell Mobile App

The mobile application acts as the user-facing terminal interface for NovaShell. It connects to the backend AI orchestrator via WebSockets to process complex commands, but also has the ability to execute hardware-level commands directly on the device using native plugins.

## Tech Stack
- **React Native (Expo)**: Cross-platform mobile framework.
- **NativeWind (Tailwind CSS)**: For styling the beautiful, minimalist terminal UI.
- **Redux Toolkit**: Manages the terminal history and UI state.
- **Expo Modules**: Accesses native device capabilities (Camera/Flashlight, Battery, Linking).

## Setup Instructions

1. **Navigate to the mobile directory**:
   ```bash
   cd apps/mobile
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Configure the WebSocket connection**:
   By default, the app expects the backend to be running on your local machine.
   If testing on an Android Emulator, the IP `10.0.2.2:8000` is used by default in `src/core/websocketManager.ts`. 
   If testing on a physical device, you will need to update the `WS_URL` in `src/core/websocketManager.ts` to your computer's local network IP address (e.g., `192.168.1.X:8000`).

4. **Start the Expo Development Server**:
   ```bash
   npx expo start
   ```

5. **Run on Device**:
   - Press `a` in the terminal to open on an Android emulator.
   - Press `i` to open on an iOS simulator (macOS only).
   - Scan the QR code with the Expo Go app on your physical device.

## Local Plugins

The mobile app includes native plugins that execute on the device when instructed by the backend AI:
- **BatteryPlugin** (`src/plugins/BatteryPlugin.ts`): Uses `expo-battery` to read device power levels.
- **FlashlightPlugin** (`src/plugins/FlashlightPlugin.ts`): Uses `expo-camera` to toggle the device torch. (Note: Flashlight functionality requires a physical device and will not work on simulators).
- **OpenAppPlugin** (`src/plugins/OpenAppPlugin.ts`): Uses React Native's `Linking` API to launch third-party apps installed on the device via URL schemes.
