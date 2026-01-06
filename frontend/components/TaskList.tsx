import { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import { taskApi } from '../lib/api';
import type { Task } from '../types/task';

interface TaskListProps {
  completedFilter?: boolean;
  priorityFilter?: string;
  searchFilter?: string;
  sortFilter?: string;
}

export default function TaskList({ completedFilter, priorityFilter, searchFilter, sortFilter }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = {};
      if (completedFilter !== undefined) params.completed = completedFilter;
      if (priorityFilter) params.priority = priorityFilter;
      if (searchFilter) params.search = searchFilter;
      if (sortFilter) params.sort = sortFilter;

      const fetchedTasks = await taskApi.getTasks(params);
      setTasks(fetchedTasks);
    } catch (err) {
      setError('Failed to fetch tasks. Please try again.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [completedFilter, priorityFilter, searchFilter, sortFilter]);

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (id: number) => {
    setTasks(prev => prev.filter(task => task.id !== id));
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="relative">
          <div className="w-20 h-20 border-8 border-purple-500/30 rounded-full animate-ping"></div>
          <div className="absolute inset-0 w-20 h-20 border-8 border-t-cyan-400 border-r-purple-500 border-b-transparent border-l-transparent rounded-full animate-spin"></div>
        </div>
        <p className="mt-8 text-2xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-cyan-300">
          Loading your tasks...
        </p>
        <p className="mt-3 text-gray-400">Hold on, magic is happening ✨</p>
      </div>
    );
  }

  if (error) {
    return (
      <div 
        className="relative overflow-hidden p-8 rounded-3xl backdrop-blur-2xl text-center"
        style={{
          background: 'rgba(30, 15, 60, 0.5)',
          border: '1px solid rgba(239, 68, 68, 0.4)',
          boxShadow: '0 0 60px rgba(239, 68, 68, 0.3), 0 20px 40px rgba(0, 0, 0, 0.6)',
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-red-600/10 to-transparent pointer-events-none" />
        <div className="relative z-10">
          <div className="text-6xl mb-6">⚠️</div>
          <h3 className="text-2xl font-bold text-red-300 mb-4">Oops! Something went wrong</h3>
          <p className="text-lg text-red-200 mb-8 max-w-md mx-auto">{error}</p>
          <button
            onClick={fetchTasks}
            className="px-8 py-4 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white font-bold text-lg rounded-2xl shadow-2xl transform hover:scale-110 hover:shadow-red-500/50 transition-all duration-500"
          >
            🔄 Try Again
          </button>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div 
        className="relative overflow-hidden p-16 rounded-3xl backdrop-blur-2xl text-center"
        style={{
          background: 'rgba(30, 20, 70, 0.4)',
          border: '1px solid rgba(139, 92, 246, 0.2)',
          boxShadow: 'inset 0 0 60px rgba(139, 92, 246, 0.1), 0 20px 40px rgba(0, 0, 0, 0.5)',
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-tr from-purple-600/5 to-cyan-600/5 pointer-events-none" />
        <div className="relative z-10">
          <div className="text-8xl mb-8 opacity-40">📝</div>
          <h3 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-cyan-300 mb-4">
            No tasks yet
          </h3>
          <p className="text-xl text-gray-300 mb-2">Your list is feeling lonely...</p>
          <p className="text-gray-400">Add a new task above to kick things off! 🚀</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-cyan-300">
          Your Tasks ({tasks.length})
        </h2>
        <div className="w-32 h-1 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"></div>
      </div>

      <div className="space-y-4">
        {tasks.map((task, index) => (
          <div
            key={task.id}
            className="animate-in slide-in-from-bottom-4 fade-in duration-700"
            style={{ animationDelay: `${index * 100}ms`, animationFillMode: 'both' }}
          >
            <TaskItem
              task={task}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
            />
          </div>
        ))}
      </div>
    </div>
  );
}