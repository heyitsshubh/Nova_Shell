import { store } from './store';
import { addMessage, setProcessing } from '../features/terminal/terminalSlice';

class WebSocketManager {
  private ws: WebSocket | null = null;
  private clientId: string;

  constructor() {
    this.clientId = Math.random().toString(36).substring(7);
  }

  connect() {
    if (this.ws) return;

    // TODO: Environment based URL
    const WS_URL = `ws://10.0.2.2:8000/ws/${this.clientId}`; // 10.0.2.2 is Android Emulator alias for localhost
    this.ws = new WebSocket(WS_URL);

    this.ws.onopen = () => {
      store.dispatch(addMessage({
        id: Date.now().toString(),
        type: 'system',
        content: 'Link to AI Orchestrator established.',
        timestamp: Date.now()
      }));
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'response') {
          store.dispatch(addMessage({
            id: Date.now().toString(),
            type: 'output',
            content: data.content,
            timestamp: Date.now()
          }));
        } else if (data.type === 'execute_plugin') {
          import('../plugins/index').then(({ pluginManager }) => {
            pluginManager.executePlugin(data.plugin, data.params || {})
              .then(res => {
                store.dispatch(addMessage({
                  id: Date.now().toString(),
                  type: 'output',
                  content: `[${data.plugin}]:\nLevel: ${res.level}%\nCharging: ${res.charging}`,
                  timestamp: Date.now()
                }));
              })
              .catch(err => {
                store.dispatch(addMessage({
                  id: Date.now().toString(),
                  type: 'error',
                  content: `[${data.plugin}] Error: ${err.message}`,
                  timestamp: Date.now()
                }));
              })
              .finally(() => {
                store.dispatch(setProcessing(false));
              });
          });
          return; // Do not unset processing state here
        } else if (data.type === 'error') {
          store.dispatch(addMessage({
            id: Date.now().toString(),
            type: 'error',
            content: data.content,
            timestamp: Date.now()
          }));
        }
      } catch (e) {
        console.error('WebSocket parse error', e);
      } finally {
        store.dispatch(setProcessing(false));
      }
    };

    this.ws.onclose = () => {
      this.ws = null;
      store.dispatch(addMessage({
        id: Date.now().toString(),
        type: 'error',
        content: 'Connection lost. Reconnecting...',
        timestamp: Date.now()
      }));
      setTimeout(() => this.connect(), 5000);
    };
  }

  send(command: string) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      store.dispatch(setProcessing(true));
      this.ws.send(JSON.stringify({ command }));
    } else {
      store.dispatch(addMessage({
        id: Date.now().toString(),
        type: 'error',
        content: 'Cannot send command. Not connected to Orchestrator.',
        timestamp: Date.now()
      }));
    }
  }
}

export const wsManager = new WebSocketManager();
