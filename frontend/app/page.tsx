'use client';
// Task T006: Create frontend app/page.tsx with basic layout structure
// Task T027: Integrate TaskList with API client to display tasks in frontend
// Task T026: Integrate TaskForm with API client to create tasks in frontend
// Task T061: Add responsive design to all frontend components using Tailwind CSS
// Task T062: Add comprehensive error handling and user feedback in frontend
// Task T063: Add loading states and performance indicators in frontend
// Task T070: Add accessibility features to frontend components

import { useState } from 'react';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';
import FilterControls from '@/components/FilterControls';

export default function Home() {
  const [search, setSearch] = useState('');
  const [completedFilter, setCompletedFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [sortFilter, setSortFilter] = useState('');

  const handleTaskCreated = () => {
    // The task list will automatically refresh due to the filter changes
    // We could add a simple visual feedback here if needed
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-4 drop-shadow-lg">
            Todo App
          </h1>
          <p className="text-xl text-gray-300">Manage your tasks with style in the dark</p>
        </header>

        <main className="space-y-8">
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
        </main>

        <footer className="mt-16 text-center text-gray-400 text-sm">
          <p>© {new Date().getFullYear()} Todo App - Full-Stack Web Application</p>
        </footer>
      </div>
    </div>
  );
}