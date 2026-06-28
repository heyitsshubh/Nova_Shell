import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface TerminalMessage {
  id: string;
  type: 'input' | 'output' | 'system' | 'error';
  content: string;
  timestamp: number;
}

interface TerminalState {
  history: TerminalMessage[];
  isProcessing: boolean;
  theme: 'cyberpunk' | 'matrix' | 'hacker';
}

const initialState: TerminalState = {
  history: [
    { id: 'boot-1', type: 'system', content: 'NovaShell OS v1.0.0 initializing...', timestamp: Date.now() },
    { id: 'boot-2', type: 'system', content: 'Connecting to orchestrator...', timestamp: Date.now() + 100 },
    { id: 'boot-3', type: 'system', content: 'Ready.', timestamp: Date.now() + 200 }
  ],
  isProcessing: false,
  theme: 'cyberpunk',
};

const terminalSlice = createSlice({
  name: 'terminal',
  initialState,
  reducers: {
    addMessage(state, action: PayloadAction<TerminalMessage>) {
      state.history.push(action.payload);
    },
    setProcessing(state, action: PayloadAction<boolean>) {
      state.isProcessing = action.payload;
    },
    clearTerminal(state) {
      state.history = [];
    }
  }
});

export const { addMessage, setProcessing, clearTerminal } = terminalSlice.actions;
export default terminalSlice.reducer;
