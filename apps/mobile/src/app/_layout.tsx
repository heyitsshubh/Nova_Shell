import { Slot } from 'expo-router';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { store } from '../core/store';
import '../../global.css';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Slot />
      </QueryClientProvider>
    </Provider>
  );
}
