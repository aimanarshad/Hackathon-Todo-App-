import { useState } from 'react';
import { taskApi } from '../lib/api';
import type { Task } from '../types/task';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (id: number) => void;
}

export default function TaskItem({ task, onTaskUpdated, onTaskDeleted }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description);
  const [priority, setPriority] = useState(task.priority || '');
  const [tags, setTags] = useState(task.tags || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggleCompletion = async () => {
    try {
      const updatedTask = await taskApi.toggleTaskCompletion(task.id);
      onTaskUpdated(updatedTask);
    } catch (err) {
      setError('Failed to update task completion status. Please try again.');
      console.error('Error toggling task completion:', err);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await taskApi.deleteTask(task.id);
      onTaskDeleted(task.id);
    } catch (err) {
      setError('Failed to delete task. Please try again.');
      console.error('Error deleting task:', err);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const updatedTask = await taskApi.updateTask(task.id, {
        title,
        description,
        priority: priority || undefined,
        tags: tags || undefined,
      });
      onTaskUpdated(updatedTask);
      setIsEditing(false);
    } catch (err) {
      setError('Failed to update task. Please try again.');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setTitle(task.title);
    setDescription(task.description);
    setPriority(task.priority || '');
    setTags(task.tags || '');
  };

  const getPriorityClass = (priority: string | null | undefined) => {
    switch (priority) {
      case 'high':
        return 'bg-gradient-to-r from-red-600 to-pink-600 text-white border border-red-500/50 shadow-lg shadow-red-500/30';
      case 'medium':
        return 'bg-gradient-to-r from-amber-500 to-orange-600 text-white border border-amber-400/50 shadow-lg shadow-amber-500/30';
      case 'low':
        return 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white border border-emerald-500/50 shadow-lg shadow-emerald-500/30';
      default:
        return 'bg-gradient-to-r from-gray-600 to-gray-700 text-gray-300 border border-gray-500/40 shadow-lg shadow-gray-600/20';
    }
  };

  return (
    <div
      className={`
        relative overflow-hidden rounded-3xl backdrop-blur-2xl transition-all duration-700
        hover:scale-[1.02] hover:shadow-2xl group
        ${task.completed 
          ? 'bg-gray-900/40 border border-gray-700/50' 
          : 'bg-gradient-to-br from-purple-900/30 via-gray-900/50 to-blue-900/30 border border-purple-500/30'
        }
      `}
      style={{
        boxShadow: task.completed 
          ? '0 10px 30px rgba(0,0,0,0.4), inset 0 0 40px rgba(139,92,246,0.05)'
          : '0 0 50px rgba(139,92,246,0.3), 0 15px 40px rgba(0,0,0,0.6), inset 0 0 60px rgba(139,92,246,0.15)',
      }}
    >
      {/* Subtle inner glow overlay */}
      {!task.completed && (
        <div className="absolute inset-0 bg-gradient-to-tr from-purple-600/10 to-cyan-600/10 pointer-events-none rounded-3xl" />
      )}

      <div className="relative p-6 md:p-8">
        {isEditing ? (
          <form onSubmit={handleUpdate} className="space-y-5">
            {error && (
              <div className="p-4 bg-red-900/60 border border-red-600/50 rounded-2xl text-red-300 backdrop-blur-sm flex items-center gap-3 shadow-lg">
                <svg className="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span className="font-medium">{error}</span>
              </div>
            )}

            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-5 py-4 rounded-xl bg-gray-900/70 border border-purple-500/30 text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 backdrop-blur-md text-lg font-semibold"
              required
              placeholder="Task title..."
            />

            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full px-5 py-4 rounded-xl bg-gray-900/70 border border-purple-500/30 text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 resize-none backdrop-blur-md"
              placeholder="Add a description..."
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="px-5 py-4 rounded-xl bg-gray-900/70 border border-purple-500/30 text-white focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 backdrop-blur-md"
              >
                <option value="">Select priority</option>
                <option value="high">High Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="low">Low Priority</option>
              </select>

              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                className="px-5 py-4 rounded-xl bg-gray-900/70 border border-purple-500/30 text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/50 focus:border-cyan-400 transition-all duration-500 backdrop-blur-md"
                placeholder="Tags (comma-separated)"
              />
            </div>

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 py-4 px-6 rounded-xl font-bold text-white bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-700 hover:to-cyan-600 shadow-xl hover:shadow-cyan-500/50 transform hover:scale-105 transition-all duration-500 disabled:opacity-70 disabled:scale-100"
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={handleCancelEdit}
                className="px-8 py-4 rounded-xl font-bold bg-gray-800/70 hover:bg-gray-700/80 text-gray-300 border border-gray-600/50 transition-all duration-300"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <>
            {error && (
              <div className="mb-5 p-4 bg-red-900/60 border border-red-600/50 rounded-2xl text-red-300 backdrop-blur-sm flex items-center gap-3 shadow-lg">
                <svg className="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span className="font-medium">{error}</span>
              </div>
            )}

            <div className="flex items-start gap-5">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggleCompletion}
                className="mt-2 w-6 h-6 text-cyan-400 rounded-lg focus:ring-cyan-400 focus:ring-4 transition-all duration-300 cursor-pointer accent-cyan-400"
              />

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-4 flex-wrap">
                  <h3 className={`
                    text-2xl font-bold transition-all duration-500
                    ${task.completed 
                      ? 'line-through text-gray-500 opacity-60' 
                      : 'text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-cyan-300'
                    }
                  `}>
                    {task.title}
                  </h3>

                  {task.priority && (
                    <span className={`
                      px-4 py-1.5 text-sm font-bold rounded-full transition-all duration-500
                      ${getPriorityClass(task.priority)}
                    `}>
                      {task.priority.toUpperCase()}
                    </span>
                  )}
                </div>

                {task.description && (
                  <p className={`
                    mt-3 text-gray-300 leading-relaxed transition-all duration-500
                    ${task.completed ? 'line-through opacity-60' : ''}
                  `}>
                    {task.description}
                  </p>
                )}

                {task.tags && task.tags.trim() !== '' && (
                  <div className="mt-4 flex flex-wrap gap-3">
                    {task.tags.split(',').map((tag, idx) => (
                      <span
                        key={idx}
                        className="px-4 py-2 bg-gradient-to-r from-purple-600/40 to-cyan-600/40 backdrop-blur-sm text-purple-200 text-sm font-medium rounded-full border border-purple-500/30 shadow-md"
                      >
                        #{tag.trim()}
                      </span>
                    ))}
                  </div>
                )}

                <div className="mt-5 text-sm text-gray-500 opacity-70">
                  Created: {new Date(task.created_at).toLocaleString()}
                  {task.updated_at !== task.created_at && (
                    <span className="ml-3">
                      • Updated: {new Date(task.updated_at).toLocaleString()}
                    </span>
                  )}
                </div>
              </div>

              <div className="flex flex-col gap-4">
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 hover:text-purple-100 border border-purple-500/30 backdrop-blur-sm transition-all duration-500 hover:scale-110 hover:shadow-lg hover:shadow-purple-500/40"
                  title="Edit task"
                >
                  Edit
                </button>

                <button
                  onClick={handleDelete}
                  className="p-3 rounded-xl bg-red-600/20 hover:bg-red-600/40 text-red-300 hover:text-red-100 border border-red-500/30 backdrop-blur-sm transition-all duration-500 hover:scale-110 hover:shadow-lg hover:shadow-red-500/40"
                  title="Delete task"
                >
                  Delete
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}