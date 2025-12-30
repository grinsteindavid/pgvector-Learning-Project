export interface Thread {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface Confidence {
  routing: number
  retrieval: number
  response: number
  overall: number
}

export interface Message {
  id: string
  thread_id: string
  role: 'user' | 'assistant'
  content: string
  route?: string
  confidence?: Confidence
  created_at: string
}

export interface ThreadWithMessages extends Thread {
  messages: Message[]
}
