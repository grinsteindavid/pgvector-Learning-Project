import type { Thread } from '../types/thread'

interface SidebarProps {
  threads: Thread[]
  activeThreadId: string | null
  onSelectThread: (id: string) => void
  onNewThread: () => void
  onDeleteThread: (id: string) => void
}

export function Sidebar({
  threads,
  activeThreadId,
  onSelectThread,
  onNewThread,
  onDeleteThread
}: SidebarProps) {
  return (
    <aside className="w-64 bg-gray-900 text-white flex flex-col h-full">
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={onNewThread}
          className="w-full bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors"
        >
          <span className="text-lg">+</span>
          <span>New Chat</span>
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto p-2">
        {threads.length === 0 ? (
          <p className="text-gray-500 text-sm text-center py-4">
            No conversations yet
          </p>
        ) : (
          <ul className="space-y-1">
            {threads.map(thread => (
              <li key={thread.id}>
                <button
                  onClick={() => onSelectThread(thread.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm truncate flex items-center justify-between group transition-colors ${
                    activeThreadId === thread.id
                      ? 'bg-gray-700 text-white'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <span className="truncate flex-1">{thread.title}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onDeleteThread(thread.id)
                    }}
                    className="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-400 ml-2 transition-opacity"
                  >
                    ×
                  </button>
                </button>
              </li>
            ))}
          </ul>
        )}
      </nav>

      <div className="p-4 border-t border-gray-700 text-xs text-gray-500">
        Clinical AI Assistant
      </div>
    </aside>
  )
}
