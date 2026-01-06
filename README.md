# Phase 2 Full-Stack Todo Web App

This project implements a full-stack todo application with FastAPI backend and Next.js frontend. The solution transforms the Phase 1 console-based todo app into a persistent, multi-user web application with PostgreSQL database.

## Features

- **Core Task Management**: Create, read, update, delete, and mark tasks as complete
- **Enhanced Features**: Priority levels (high/medium/low) and tags for better organization
- **Advanced Organization**: Search, filter, and sort functionality
- **Responsive UI**: Works on desktop and mobile devices
- **API-First**: Clean REST API with full CRUD operations

## Tech Stack

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Database**: PostgreSQL (with Neon compatibility)

## API Endpoints

- `GET /api/tasks` - List all tasks with optional filters and sorting
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Environment Variables

Create a `.env` file in the project root with:

```
DATABASE_URL=postgresql://user:password@localhost/todo_db
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Running the Application

### Backend (API Server)

1. Navigate to the `backend` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `uvicorn main:app --reload`
4. The API will be available at `http://localhost:8000`

### Frontend (Web App)

1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. The web app will be available at `http://localhost:3000`

## Database Setup

1. Ensure PostgreSQL is running
2. Update the DATABASE_URL in your .env file
3. The database tables will be created automatically on startup

## Development

The application follows a spec-driven development approach. All code is generated from the specifications in the `specs/` directory.
