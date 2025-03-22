import React, { createContext, useContext, useReducer, useCallback, useEffect } from 'react';
import { ChatMessage, ChatContextType } from '../types';
import { useAuth } from './AuthContext';

type ChatAction =
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'CLEAR_CHAT' }
  | { type: 'LOAD_MESSAGES'; payload: ChatMessage[] };

const ChatContext = createContext<ChatContextType | null>(null);

const STORAGE_KEY = 'chat_messages';

const chatReducer = (state: ChatMessage[], action: ChatAction): ChatMessage[] => {
  switch (action.type) {
    case 'ADD_MESSAGE':
      const newState = [...state, action.payload];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newState));
      return newState;
    case 'CLEAR_CHAT':
      localStorage.removeItem(STORAGE_KEY);
      return [];
    case 'LOAD_MESSAGES':
      return action.payload;
    default:
      return state;
  }
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [messages, dispatch] = useReducer(chatReducer, []);
  const { user } = useAuth();

  // Load messages from localStorage on mount
  useEffect(() => {
    const savedMessages = localStorage.getItem(STORAGE_KEY);
    if (savedMessages) {
      const parsedMessages = JSON.parse(savedMessages).map((msg: any) => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      }));
      dispatch({ type: 'LOAD_MESSAGES', payload: parsedMessages });
    }
  }, []);

  const sendMessage = useCallback(
    async (message: string) => {
      if (!user) return;

      // Add user message
      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        userId: user.id,
        message,
        timestamp: new Date(),
        isUser: true,
      };
      dispatch({ type: 'ADD_MESSAGE', payload: userMessage });

      // Call the Python API to get the chatbot response
      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message }),
        });

        const data = await response.json();
        const botMessage: ChatMessage = {
          id: crypto.randomUUID(),
          userId: 'system',
          message: data.response,
          timestamp: new Date(),
          isUser: false,
        };
        dispatch({ type: 'ADD_MESSAGE', payload: botMessage });
      } catch (error) {
        const errorMessage: ChatMessage = {
          id: crypto.randomUUID(),
          userId: 'system',
          message: "Sorry, something went wrong. Please try again.",
          timestamp: new Date(),
          isUser: false,
        };
        dispatch({ type: 'ADD_MESSAGE', payload: errorMessage });
      }
    },
    [user]
  );

  const clearChat = useCallback(() => {
    dispatch({ type: 'CLEAR_CHAT' });
  }, []);

  return (
    <ChatContext.Provider value={{ messages, sendMessage, clearChat }}>
      {children}
    </ChatContext.Provider>
  );
};