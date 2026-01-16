// frontend/lib/api.ts
// Task T015, T052, T053, T054 – Final Production-Ready API Client

import type { Task } from '@/types/task';

// Use environment variable in production, fallback for local dev
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

// Helper to build query string safely
const buildQuery = (params?: Record<string, string | boolean | undefined>) => {
  const searchParams = new URLSearchParams();
  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      searchParams.append(key, value.toString());
    }
  });
  const query = searchParams.toString();
  return query ? `?${query}` : '';
};

export const taskApi = {
  // GET /api/tasks → with full search, filter, sort support
  getTasks: async (params?: {
    completed?: boolean;
    priority?: string;
    search?: string;
    sort?: string;
  }): Promise<Task[]> => {
    const url = `${API_BASE_URL}/tasks${buildQuery(params )}`;
    const response = await fetch(url, { cache: 'no-store' }); // Important for real-time

    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.status}`);
    }
    return response.json();
  },

  // POST /api/tasks
  createTask: async (task: Omit<Task, 'id' | 'created_at' | 'updated_at'>): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task),
    });

    if (!response.ok) throw new Error(`Create failed: ${response.status}`);
    return response.json();
  },

  // GET /api/tasks/{id}
  getTask: async (id: number): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`);
    if (!response.ok) throw new Error(`Task not found: ${response.status}`);
    return response.json();
  },

  // PUT /api/tasks/{id}
  updateTask: async (id: number, updates: Partial<Task>): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!response.ok) throw new Error(`Update failed: ${response.status}`);
    return response.json();
  },

  // DELETE /api/tasks/{id}
  deleteTask: async (id: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error(`Delete failed: ${response.status}`);
  },

  // PATCH /api/tasks/{id}/complete
  toggleTaskCompletion: async (id: number): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}/complete`, {
      method: 'PATCH',
    });
    if (!response.ok) throw new Error(`Toggle failed: ${response.status}`);
    return response.json();
  },
};