import React, { useState, useRef, useEffect } from 'react';
import { searchQuery } from './services/api';
import './App.css';

interface Message {
  sender: 'user' | 'ai';
  text: string;
}

const App: React.FC = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!query.trim()) return;
    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setLoading(true);
    setError('');
    try {
      const aiResponse = await searchQuery(query);
      setMessages((prev) => [
        ...prev,
        { sender: 'ai', text: aiResponse },
      ]);
    } catch (err) {
      setError('Network or server error.');
    }
    setLoading(false);
    setQuery('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="chat-root">
      <div className="chat-container">
        <h1 className="chat-title">AI Knowledge Chat</h1>
        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${msg.sender === 'user' ? 'user' : 'ai'}`}
            >
              <span>{msg.text}</span>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {error && <div className="chat-error">{error}</div>}
        <div className="chat-input-row">
          <input
            type="text"
            placeholder="Type your question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            className="chat-input"
            autoFocus
          />
          <button onClick={handleSend} disabled={loading || !query.trim()} className="chat-send-btn">
            {loading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;