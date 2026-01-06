// Task T069: Add TypeScript type definitions for all frontend API interactions
export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority?: string | null; // "high", "medium", "low"
  tags?: string | null; // comma-separated
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  user_id?: number | null;
}