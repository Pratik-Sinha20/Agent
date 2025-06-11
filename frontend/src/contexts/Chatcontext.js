import React, { createContext, useContext, useState, useEffect } from 'react';
import { auth } from '../firebase-config'; // Your Firebase config

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (auth.currentUser) {
      setSessionId(auth.currentUser.uid);
    }
  }, []);

  const sendMessage = async (message) => {
    if (!sessionId) return;

    setIsLoading(true);
    
    // Add user message to UI
    const userMessage = { role: 'user', content: message, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await auth.currentUser.getIdToken()}`
        },
        body: JSON.stringify({
          user_id: sessionId,
          message: message
        })
      });

      const data = await response.json();
      
      // Add bot response to UI
      const botMessage = { 
        role: 'assistant', 
        content: data.response, 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.', 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContext.Provider value={{ 
      messages, 
      sendMessage, 
      isLoading, 
      sessionId 
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }
  return context;
};
