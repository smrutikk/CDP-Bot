import React, { useState, useRef, useEffect } from 'react';
import { Send, RotateCcw } from 'lucide-react';
import './App.css';


const ChatMessage = ({ message, type }) => (
  <div className={`chat-message ${type === 'user' ? 'user' : 'bot'}`}>
    <div className="chat-message-content">
      {message}
    </div>
  </div>
);

const CDPChatbot = () => {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: "Hello! I'm your CDP assistant. Ask me how-to questions about Segment, mParticle, Lytics, or Zeotap!"
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = inputValue.trim();
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Make API call to Flask backend
      const response = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage }),
      });

      const data = await response.json();

      if (data.answer) {
        setMessages(prev => [...prev, { type: 'bot', text: data.answer }]);
      } else {
        setMessages(prev => [...prev, { type: 'bot', text: 'Sorry, I could not process your request.' }]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { type: 'bot', text: 'Something went wrong. Please try again later.' }]);
    }

    setIsLoading(false);
  };

  const handleReset = () => {
    setMessages([{
      type: 'bot',
      text: "Hello! I'm your CDP assistant. Ask me how-to questions about Segment, mParticle, Lytics, or Zeotap!"
    }]);
  };

  return (
    <div className="chat-container">
      <div className="card-header">
        <div className="flex justify-between items-center">
          <h2 className="card-title">CDP Assistant</h2>
          <button onClick={handleReset} className="btn">
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message.text} type={message.type} />
          ))}
          {isLoading && (
            <div className="loading-message">
              <div className="chat-message-content">Typing...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <div className="flex gap-2">
          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about CDPs..."
            className="input-field"
          />
          <button type="submit" className="btn">
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default CDPChatbot;
