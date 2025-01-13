import React, { useState, useRef, useEffect } from 'react';
import { Send, RotateCcw } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const ChatMessage = ({ message, type }) => (
  <div className={`flex ${type === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
    <div className={`rounded-lg px-4 py-2 max-w-[80%] ${
      type === 'user' 
        ? 'bg-blue-600 text-white' 
        : 'bg-gray-100 text-gray-900'
    }`}>
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

    // Simulate bot response - replace with actual API call
    setTimeout(() => {
      let botResponse;
      if (userMessage.toLowerCase().includes('segment')) {
        botResponse = "To set up a new source in Segment:\n1. Navigate to Connections > Sources\n2. Click 'Add Source'\n3. Select your source type\n4. Configure the source settings\n5. Verify the connection";
      } else if (userMessage.toLowerCase().includes('mparticle')) {
        botResponse = "To create a user profile in mParticle:\n1. Go to User Profiles section\n2. Click 'Create New Profile'\n3. Define profile attributes\n4. Set identity mappings\n5. Save the profile";
      } else {
        botResponse = "I can help you with questions about Segment, mParticle, Lytics, or Zeotap. Please specify which CDP you're asking about.";
      }
      
      setMessages(prev => [...prev, { type: 'bot', text: botResponse }]);
      setIsLoading(false);
    }, 1000);
  };

  const handleReset = () => {
    setMessages([{
      type: 'bot',
      text: "Hello! I'm your CDP assistant. Ask me how-to questions about Segment, mParticle, Lytics, or Zeotap!"
    }]);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto h-[600px] flex flex-col">
      <CardHeader className="border-b">
        <div className="flex justify-between items-center">
          <CardTitle>CDP Assistant</CardTitle>
          <Button variant="outline" size="icon" onClick={handleReset}>
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message.text} type={message.type} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                Typing...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </CardContent>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about CDPs..."
            className="flex-1"
          />
          <Button type="submit" className="px-6">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default CDPChatbot;