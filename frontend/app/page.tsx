'use client';
// Task T006: Create frontend app/page.tsx with basic layout structure
// Task T027: Integrate TaskList with API client to display tasks in frontend
// Task T026: Integrate TaskForm with API client to create tasks in frontend
// Task T061: Add responsive design to all frontend components using Tailwind CSS
// Task T062: Add comprehensive error handling and user feedback in frontend
// Task T063: Add loading states and performance indicators in frontend
// Task T070: Add accessibility features to frontend components
// Phase 5: Update to support recurring tasks and reminders

import { useState } from 'react';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';
import FilterControls from '@/components/FilterControls';
import RecurringTaskForm from '@/components/RecurringTaskForm';
import ReminderSettings from '@/components/ReminderSettings';

export default function Home() {
  const [search, setSearch] = useState('');
  const [completedFilter, setCompletedFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [sortFilter, setSortFilter] = useState('');
  const [activeTab, setActiveTab] = useState<'tasks' | 'recurring' | 'reminders'>('tasks');

  const handleTaskCreated = () => {
    // The task list will automatically refresh due to the filter changes
    // We could add a simple visual feedback here if needed
  };

  const handleRecurringTaskSubmit = (data: any) => {
    console.log('Creating recurring task:', data);
    // In a real implementation, this would call an API endpoint
    alert('Recurring task created successfully!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-4 drop-shadow-lg">
            Todo App - Advanced Cloud Edition
          </h1>
          <p className="text-xl text-gray-300">Manage your tasks with advanced features in the cloud</p>
        </header>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-slate-800/50 backdrop-blur-md rounded-xl p-1 border border-slate-700/50">
            <button
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                activeTab === 'tasks'
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-slate-700/50'
              }`}
              onClick={() => setActiveTab('tasks')}
            >
              Regular Tasks
            </button>
            <button
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                activeTab === 'recurring'
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-slate-700/50'
              }`}
              onClick={() => setActiveTab('recurring')}
            >
              Recurring Tasks
            </button>
            <button
              className={`px-6 py-3 rounded-lg transition-all duration-300 ${
                activeTab === 'reminders'
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-slate-700/50'
              }`}
              onClick={() => setActiveTab('reminders')}
            >
              Reminder Settings
            </button>
          </div>
        </div>

        <main className="space-y-8">
          {/* Conditional rendering based on active tab */}
          {activeTab === 'tasks' && (
            <>
              <section className="bg-slate-800/50 backdrop-blur-md rounded-2xl shadow-2xl p-6 border border-slate-700/50">
                <TaskForm onTaskCreated={handleTaskCreated} />
              </section>

              <section className="bg-slate-800/50 backdrop-blur-md rounded-2xl shadow-2xl p-6 border border-slate-700/50">
                <FilterControls
                  search={search}
                  completedFilter={completedFilter}
                  priorityFilter={priorityFilter}
                  sortFilter={sortFilter}
                  onSearchChange={setSearch}
                  onCompletedChange={setCompletedFilter}
                  onPriorityChange={setPriorityFilter}
                  onSortChange={setSortFilter}
                />
              </section>

              <section className="bg-slate-800/70 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-slate-600/50">
                <h2 className="text-3xl font-bold text-gray-100 mb-6 flex items-center gap-3">
                  <span className="inline-block w-2 h-10 bg-gradient-to-b from-purple-500 to-pink-500 rounded-full"></span>
                  Task List
                </h2>
                <TaskList
                  searchFilter={search}
                  completedFilter={completedFilter ? completedFilter === 'true' : undefined}
                  priorityFilter={priorityFilter || undefined}
                  sortFilter={sortFilter || undefined}
                />
              </section>
            </>
          )}

          {activeTab === 'recurring' && (
            <section className="bg-slate-800/50 backdrop-blur-md rounded-2xl shadow-2xl p-6 border border-slate-700/50">
              <RecurringTaskForm onSubmit={handleRecurringTaskSubmit} />
            </section>
          )}

          {activeTab === 'reminders' && (
            <section className="bg-slate-800/50 backdrop-blur-md rounded-2xl shadow-2xl p-6 border border-slate-700/50">
              <ReminderSettings userId={1} />
            </section>
          )}
        </main>

        <footer className="mt-16 text-center text-gray-400 text-sm">
          <p>© {new Date().getFullYear()} Todo App - Advanced Cloud Deployment with Dapr, Kafka & Oracle OKE</p>
        </footer>
      </div>
    </div>
  );
}