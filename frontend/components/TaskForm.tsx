import { useState } from 'react';
import { taskApi } from '../lib/api';
import type { Task } from '../types/task';

interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<string | undefined>('');
  const [tags, setTags] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const newTask = await taskApi.createTask({
        title: title.trim(),
        description,
        priority: priority || undefined,
        tags: tags || undefined,
        completed: false
      });

      onTaskCreated(newTask);
      setTitle('');
      setDescription('');
      setPriority('');
      setTags('');
    } catch (err) {
      setError('Failed to create task. Please try again.');
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="relative overflow-hidden mb-10 p-8 md:p-10 rounded-3xl backdrop-blur-2xl"
      style={{
        background: 'rgba(30, 15, 60, 0.45)', // Semi-transparent deep purple for contrast
        border: '1px solid rgba(139, 92, 246, 0.3)',
        boxShadow: `
          0 0 40px rgba(139, 92, 246, 0.4),
          0 0 80px rgba(59, 130, 246, 0.25),
          inset 0 0 60px rgba(139, 92, 246, 0.1),
          0 20px 40px rgba(0, 0, 0, 0.8)
        `,
      }}
    >
      {/* Intense inner glow overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 via-transparent to-blue-600/20 pointer-events-none rounded-3xl" />

      <h2 className="relative text-3xl md:text-4xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-cyan-300 tracking-tight drop-shadow-2xl">
        Create New Task
      </h2>

      {error && (
        <div className="relative mb-6 p-4 bg-red-900/60 border border-red-600/50 rounded-xl text-red-300 backdrop-blur-sm flex items-center gap-3 shadow-lg">
          <svg className="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          <span className="font-medium">{error}</span>
        </div>
      )}

      <div className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-semibold text-purple-200 mb-2">
            Title <span className="text-red-400">*</span>
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-5 py-4 rounded-xl bg-gray-900/60 border border-purple-500/30 text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 backdrop-blur-md"
            placeholder="Enter an epic task title..."
            required
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-semibold text-purple-200 mb-2">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
            className="w-full px-5 py-4 rounded-xl bg-gray-900/60 border border-purple-500/30 text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 resize-none backdrop-blur-md"
            placeholder="What's this task all about?"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="priority" className="block text-sm font-semibold text-purple-200 mb-2">
              Priority Level
            </label>
            <select
              id="priority"
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              className="w-full px-5 py-4 rounded-xl bg-gray-900/60 border border-purple-500/30 text-white focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 backdrop-blur-md appearance-none cursor-pointer"
              style={{
                backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%238b5cf6' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                backgroundPosition: 'right 1rem center',
                backgroundRepeat: 'no-repeat',
                backgroundSize: '12px',
              }}
            >
              <option value="">Choose priority</option>
              <option value="high">🔴 High</option>
              <option value="medium">🟡 Medium</option>
              <option value="low">🟢 Low</option>
            </select>
          </div>

          <div>
            <label htmlFor="tags" className="block text-sm font-semibold text-purple-200 mb-2">
              Tags (comma-separated)
            </label>
            <input
              type="text"
              id="tags"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              className="w-full px-5 py-4 rounded-xl bg-gray-900/60 border border-purple-500/30 text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 backdrop-blur-md"
              placeholder="work, urgent, design, fun"
            />
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="relative mt-10 w-full py-5 px-6 rounded-xl font-bold text-lg tracking-wide overflow-hidden transform transition-all duration-700 hover:scale-105 hover:shadow-2xl disabled:scale-100 disabled:opacity-70"
        style={{
          background: 'linear-gradient(135deg, #c084fc 0%, #22d3ee 100%)',
          boxShadow: '0 0 40px rgba(34, 211, 238, 0.6), 0 10px 30px rgba(192, 132, 252, 0.5)',
        }}
      >
        <span className="relative z-10 text-white drop-shadow-lg">
          {loading ? 'Creating Task...' : 'Add Task'}
        </span>
      </button>
    </form>
  );
}