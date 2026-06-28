import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import terminalReducer from '../features/terminal/terminalSlice';

export const store = configureStore({
  reducer: {
    terminal: terminalReducer
  },
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
