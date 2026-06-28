import  { useEffect, useState, useRef } from 'react';
import { View, Text, TextInput, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../core/store';
import { addMessage, clearTerminal, TerminalMessage } from '../features/terminal/terminalSlice';
import { wsManager } from '../core/websocketManager';

export default function TerminalScreen() {
  const [input, setInput] = useState('');
  const history = useSelector((state: RootState) => state.terminal.history);
  const isProcessing = useSelector((state: RootState) => state.terminal.isProcessing);
  const dispatch = useDispatch();
  const flatListRef = useRef<FlatList>(null);

  useEffect(() => {
    wsManager.connect();
  }, []);

  const handleCommand = () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    // Echo input locally
    dispatch(addMessage({
      id: Date.now().toString(),
      type: 'input',
      content: trimmed,
      timestamp: Date.now()
    }));

    // Handle local commands
    if (trimmed.toLowerCase() === 'clear') {
      dispatch(clearTerminal());
    } else if (trimmed.toLowerCase() === 'help') {
      dispatch(addMessage({
        id: Date.now().toString(),
        type: 'output',
        content: 'NovaShell Local Commands:\nclear - Clear terminal screen\nhelp - Show this message\nAll other commands are sent to the AI Orchestrator.',
        timestamp: Date.now()
      }));
    } else {
      // Send to backend Orchestrator
      wsManager.send(trimmed);
    }

    setInput('');
  };

  const renderItem = ({ item }: { item: TerminalMessage }) => {
    let colorClass = 'text-white';
    if (item.type === 'system') colorClass = 'text-blue-400';
    if (item.type === 'error') colorClass = 'text-red-500';
    if (item.type === 'input') colorClass = 'text-green-500';

    return (
      <View className="mb-2">
        {item.type === 'input' ? (
          <Text className="text-green-500 font-mono">nova {item.content}</Text>
        ) : (
          <Text className={`${colorClass} font-mono`}>{item.content}</Text>
        )}
      </View>
    );
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
      className="flex-1 bg-black p-4"
    >
      <FlatList
        ref={flatListRef}
        data={history}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
      />
      
      <View className="flex-row items-center border-t border-gray-800 pt-3 pb-3">
        <Text className="text-green-500 font-mono mr-2">nova</Text>
        <TextInput 
          className="flex-1 text-white font-mono text-base"
          placeholder={isProcessing ? "Processing..." : "Enter command or intent..."}
          placeholderTextColor="#4b5563"
          autoCapitalize="none"
          autoCorrect={false}
          value={input}
          onChangeText={setInput}
          onSubmitEditing={handleCommand}
          editable={!isProcessing}
        />
      </View>
    </KeyboardAvoidingView>
  );
}
