import { Chat } from './components/Chat'
import { Sidebar } from './components/Sidebar'
import { useThreads } from './hooks/useThreads'

function App() {
  const {
    threads,
    activeThreadId,
    messages,
    isLoading,
    createThread,
    selectThread,
    deleteThread,
    sendMessage
  } = useThreads()

  return (
    <div className="h-full flex">
      <Sidebar
        threads={threads}
        activeThreadId={activeThreadId}
        onSelectThread={selectThread}
        onNewThread={createThread}
        onDeleteThread={deleteThread}
      />
      <main className="flex-1">
        <Chat
          messages={messages}
          isLoading={isLoading}
          onSendMessage={sendMessage}
          hasActiveThread={activeThreadId !== null}
        />
      </main>
    </div>
  )
}

export default App
