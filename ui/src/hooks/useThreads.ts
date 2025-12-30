import { useState, useEffect, useCallback } from 'react'
import type { Thread, Message, ThreadWithMessages, Confidence } from '../types/thread'

const API_BASE = '/api'

export function useThreads() {
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fetchThreads = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/threads`)
      if (res.ok) {
        const data = await res.json()
        setThreads(data)
      }
    } catch (error) {
      console.error('Failed to fetch threads:', error)
    }
  }, [])

  const createThread = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/threads`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New Chat' })
      })
      if (res.ok) {
        const thread = await res.json()
        setThreads(prev => [thread, ...prev])
        setActiveThreadId(thread.id)
        setMessages([])
        return thread
      }
    } catch (error) {
      console.error('Failed to create thread:', error)
    }
    return null
  }, [])

  const selectThread = useCallback(async (threadId: string) => {
    setActiveThreadId(threadId)
    try {
      const res = await fetch(`${API_BASE}/threads/${threadId}`)
      if (res.ok) {
        const data: ThreadWithMessages = await res.json()
        setMessages(data.messages || [])
      }
    } catch (error) {
      console.error('Failed to fetch thread:', error)
    }
  }, [])

  const deleteThread = useCallback(async (threadId: string) => {
    try {
      const res = await fetch(`${API_BASE}/threads/${threadId}`, {
        method: 'DELETE'
      })
      if (res.ok) {
        setThreads(prev => prev.filter(t => t.id !== threadId))
        if (activeThreadId === threadId) {
          setActiveThreadId(null)
          setMessages([])
        }
      }
    } catch (error) {
      console.error('Failed to delete thread:', error)
    }
  }, [activeThreadId])

  const sendMessage = useCallback(async (content: string) => {
    if (!activeThreadId || isLoading) return

    setIsLoading(true)

    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      thread_id: activeThreadId,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])

    const assistantMessage: Message = {
      id: `temp-${Date.now() + 1}`,
      thread_id: activeThreadId,
      role: 'assistant',
      content: '',
      created_at: new Date().toISOString()
    }
    setMessages(prev => [...prev, assistantMessage])

    try {
      const res = await fetch(`${API_BASE}/threads/${activeThreadId}/query/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: content })
      })

      if (!res.ok) throw new Error('Request failed')

      const reader = res.body?.getReader()
      const decoder = new TextDecoder()
      if (!reader) throw new Error('No response body')

      let accumulatedContent = ''
      let route = ''
      let confidence: Confidence | undefined

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const event = JSON.parse(data)
              if (event.node === 'supervisor' && event.data.route) {
                route = event.data.route
              }
              if (event.data.response) {
                accumulatedContent = event.data.response
              }
              if (event.data.confidence) {
                confidence = event.data.confidence
              }

              setMessages(prev => prev.map(msg =>
                msg.id === assistantMessage.id
                  ? { ...msg, content: accumulatedContent, route, confidence }
                  : msg
              ))
            } catch {
              // Skip invalid JSON
            }
          }
        }
      }

      fetchThreads()

    } catch (error) {
      console.error('Failed to send message:', error)
      setMessages(prev => prev.map(msg =>
        msg.id === assistantMessage.id
          ? { ...msg, content: 'Error: Failed to get response' }
          : msg
      ))
    } finally {
      setIsLoading(false)
    }
  }, [activeThreadId, isLoading, fetchThreads])

  useEffect(() => {
    fetchThreads()
  }, [fetchThreads])

  return {
    threads,
    activeThreadId,
    messages,
    isLoading,
    createThread,
    selectThread,
    deleteThread,
    sendMessage
  }
}
