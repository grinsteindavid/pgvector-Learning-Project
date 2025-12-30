import { useRef, useEffect, useState } from 'react'
import type { Message } from '../types/thread'

interface ChatProps {
  messages: Message[]
  isLoading: boolean
  onSendMessage: (content: string) => void
  hasActiveThread: boolean
}

export function Chat({ messages, isLoading, onSendMessage, hasActiveThread }: ChatProps) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return
    onSendMessage(input.trim())
    setInput('')
  }

  if (!hasActiveThread) {
    return (
      <div className="flex flex-col h-full items-center justify-center bg-gray-50">
        <div className="text-center text-gray-400">
          <h2 className="text-2xl font-semibold mb-2">Clinical AI Assistant</h2>
          <p className="text-sm">Select a chat or create a new one to get started</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">How can I help you today?</p>
            <p className="text-sm mt-2">Ask about clinical tools, healthcare organizations, or workflow optimization</p>
          </div>
        )}

        {messages.map(message => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border border-gray-200 text-gray-800'
              }`}
            >
              {message.route && (
                <span className="inline-block text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded mb-2">
                  Route: {message.route}
                </span>
              )}
              <p className="whitespace-pre-wrap">{message.content}</p>
              {message.content === '' && message.role === 'assistant' && (
                <span className="inline-block w-2 h-4 bg-gray-400 animate-pulse" />
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t bg-white p-4">
        <div className="flex gap-3 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about clinical tools, healthcare AI, or workflow optimization..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  )
}
