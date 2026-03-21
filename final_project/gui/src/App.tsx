import { useEffect, useRef, useState } from 'react'
import './App.css'

interface Message {
  id: number
  sender: 'agent' | 'user'
  text: string
}

let nextId = 0

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [connected, setConnected] = useState(false)
  const [statusText, setStatusText] = useState('')
  const wsRef = useRef<WebSocket | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    function connect() {
      const ws = new WebSocket('ws://localhost:8765')
      wsRef.current = ws

      ws.onopen = () => setConnected(true)

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'status') {
          setStatusText(data.text)
        } else {
          setStatusText('')
          setMessages((prev) => [
            ...prev,
            { id: nextId++, sender: 'agent', text: data.text.trim() },
          ])
        }
      }

      ws.onclose = () => {
        setConnected(false)
        setTimeout(connect, 2000)
      }

      ws.onerror = () => ws.close()
    }

    connect()
    return () => wsRef.current?.close()
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function handleInputChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setInput(e.target.value)
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = el.scrollHeight + 'px'
    }
  }

  function startNew() {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return
    setMessages([])
    setInput('')
    setStatusText('')
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
    wsRef.current.send(JSON.stringify({ type: 'restart' }))
  }

  function submit() {
    const text = input.trim()
    if (!text || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return
    setMessages((prev) => [...prev, { id: nextId++, sender: 'user', text }])
    // DO Not clear input immediately to allow user to change their input iteratively
    wsRef.current.send(JSON.stringify({ text }))
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className="chat-root">
      <header className="chat-header">
        <div className="header-left">
          <h1>Logic Helper</h1>
          <span className={`status ${connected ? 'online' : 'offline'}`}>
            {connected ? 'Connected' : 'Connecting…'}
          </span>
        </div>
        <button className="end-btn" onClick={startNew} disabled={!connected}>
          Start New
        </button>
      </header>

      <main className="message-list">
        {messages.length === 0 && (
          <p className="empty">Waiting for the agent to start…</p>
        )}
        {messages.map((msg) => (
          <div key={msg.id} className={`bubble ${msg.sender}`}>
            <span className="label">{msg.sender === 'agent' ? 'Agent' : 'You'}</span>
            <p>{msg.text}</p>
          </div>
        ))}
        <div ref={bottomRef} />
      </main>

      {statusText && (
        <div className="status-bar">
          <span className="status-dot" />
          {statusText}
        </div>
      )}

      <footer className="input-row">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Type a message… (Ctrl+Enter to send)"
        />
        <button onClick={submit} disabled={!connected}>
          Send
        </button>
      </footer>
    </div>
  )
}
