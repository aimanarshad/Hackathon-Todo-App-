'use client'

import { useState, useRef, useEffect } from 'react'
import Head from 'next/head'

interface Message {
  id?: number
  role: 'user' | 'assistant'
  content: string
}

export default function ChatPage() {
  const [inputValue, setInputValue] = useState('')
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content:
        "Hello! I'm your smart AI Todo assistant ✨\n\n" +
        "You can ask me to:\n" +
        "• Add a task\n" +
        "• Show all tasks\n" +
        "• Complete a task\n" +
        "• Delete a task\n" +
        "• Update a task",
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<number | null>(null)

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  // Simple formatter to make assistant responses look clean with bullets
  const formatAssistantMessage = (text: string) => {
    const lines = text.split('\n')
    return lines.map((line, i) => {
      const trimmed = line.trim()
      if (trimmed.startsWith('•') || trimmed.startsWith('-') || trimmed.match(/^\d+\./)) {
        return (
          <li key={i} className="ml-5 text-purple-200">
            {trimmed.replace(/^[-•]|\d+\.\s*/g, '').trim()}
          </li>
        )
      }
      if (trimmed === '') return <br key={i} />
      return (
        <p key={i} className="mb-1.5">
          {line}
        </p>
      )
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = { role: 'user', content: inputValue }
    setMessages((prev) => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId,
        }),
      })

      if (!res.ok) throw new Error('Failed')

      const data = await res.json()

      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id)
      }

      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Something went wrong... Please try again 😔' },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>AI Todo • Neon Style</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-fuchsia-950 text-gray-100">
        <div className="max-w-4xl mx-auto flex flex-col h-screen px-4 py-6">
          <div className="flex-1 flex flex-col bg-black/30 backdrop-blur-xl rounded-3xl border border-purple-500/20 shadow-2xl overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-900/80 to-fuchsia-900/70 p-6 border-b border-purple-500/20">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
                AI Todo Assistant
              </h1>
              <p className="mt-1.5 text-purple-200/90">
                Manage tasks with natural language • Just talk to me
              </p>
            </div>

            {/* Messages area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`
                      max-w-[85%] rounded-2xl px-6 py-4
                      backdrop-blur-sm border border-white/10
                      ${
                        msg.role === 'user'
                          ? 'bg-gradient-to-br from-purple-700/70 to-fuchsia-700/60 text-white rounded-br-none'
                          : 'bg-black/40 text-purple-100 rounded-bl-none'
                      }
                    `}
                  >
                    {msg.role === 'assistant' ? (
                      <ul className="space-y-2 list-none">{formatAssistantMessage(msg.content)}</ul>
                    ) : (
                      <div className="whitespace-pre-wrap leading-relaxed">{msg.content}</div>
                    )}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-black/40 backdrop-blur-xl rounded-2xl px-7 py-5 border border-purple-500/20">
                    <div className="flex gap-3">
                      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" />
                      <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce delay-150" />
                      <div className="w-3 h-3 bg-cyan-400 rounded-full animate-bounce delay-300" />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-6 border-t border-purple-500/20 bg-black/40">
              <form onSubmit={handleSubmit} className="relative">
                <input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  disabled={isLoading}
                  placeholder="What would you like to do today..."
                  className="
                    w-full px-6 py-5 rounded-full text-base
                    bg-white/5 border border-purple-500/30 text-white
                    placeholder:text-purple-300/60
                    focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-500/40
                    transition-all
                  "
                  onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSubmit(e))}
                />
                <button
                  type="submit"
                  disabled={isLoading || !inputValue.trim()}
                  className="
                    absolute right-3 top-1/2 -translate-y-1/2
                    px-7 py-3 rounded-full text-sm font-medium
                    bg-gradient-to-r from-purple-600 to-pink-600
                    hover:from-purple-700 hover:to-pink-700
                    disabled:opacity-50
                    transition-all shadow-lg
                  "
                >
                  Send
                </button>
              </form>

              <p className="text-center text-sm text-purple-300/60 mt-4">
                Try: "add task gym at 7pm" • "show my tasks" • "complete task 4"
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}