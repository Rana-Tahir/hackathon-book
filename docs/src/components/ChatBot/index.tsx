import React, { useState, useRef, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './ChatBot.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: { chapter: string; section: string; relevance: number }[];
}

interface ChatBotProps {
  currentChapter?: string;
  currentModule?: number;
  selectedText?: string;
  onClearSelection?: () => void;
}

export default function ChatBot({
  currentChapter,
  currentModule,
  selectedText,
  onClearSelection,
}: ChatBotProps) {
  const { siteConfig } = useDocusaurusContext();
  const API_BASE = (siteConfig.customFields?.chatbotApiUrl as string) || 'http://localhost:8000';

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-open and prefill when text is selected
  useEffect(() => {
    if (selectedText) {
      setIsOpen(true);
    }
  }, [selectedText]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: Message = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: text,
          selected_text: selectedText || null,
          chapter: currentChapter || null,
          module: currentModule || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setSessionId(data.session_id);

      const assistantMsg: Message = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
      };
      setMessages((prev) => [...prev, assistantMsg]);

      // Clear selected text after using it
      if (selectedText && onClearSelection) {
        onClearSelection();
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I could not connect to the backend. Please try again later.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating button */}
      <button
        className={styles.fab}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chatbot' : 'Open chatbot'}
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className={styles.panel}>
          <div className={styles.header}>
            <span className={styles.headerTitle}>
              <span className={styles.headerDot} />
              AI Book Assistant
            </span>
            <button onClick={() => setIsOpen(false)} className={styles.closeBtn}>
              ✕
            </button>
          </div>

          {/* Selected text indicator */}
          {selectedText && (
            <div className={styles.selectedText}>
              <small>Asking about selected text:</small>
              <p>{selectedText.slice(0, 120)}{selectedText.length > 120 ? '...' : ''}</p>
            </div>
          )}

          <div className={styles.messages}>
            {messages.length === 0 && (
              <div className={styles.placeholder}>
                Ask me anything about the book content. Select text on the page
                for context-specific answers.
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`${styles.message} ${styles[msg.role]}`}>
                <div className={styles.bubble}>{msg.content}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    {msg.sources.map((s, j) => (
                      <small key={j}>
                        📖 {s.chapter} — {s.section}
                      </small>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.bubble}>Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.inputArea}>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about the book..."
              rows={1}
              disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading || !input.trim()}>
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}
