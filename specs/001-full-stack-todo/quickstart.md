# Quickstart Guide: Phase 2 Full-Stack Todo Web App

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- UV package manager

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env to add your DATABASE_URL
```

### 3. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
# or
yarn install
# or
pnpm install
```

### 4. Database Setup
```bash
# From backend directory with virtual environment activated
cd backend
python -c "from database import engine, create_db_and_tables; create_db_and_tables()"
```

### 5. Running the Applications

**Backend (API)**:
```bash
# From backend directory
cd backend
uvicorn main:app --reload
```
Backend will run on `http://localhost:8000`

**Frontend (Web App)**:
```bash
# From frontend directory
cd frontend
npm run dev
# or
yarn dev
# or
pnpm dev
```
Frontend will run on `http://localhost:3000`

## API Endpoints

- `GET /tasks` - List all tasks with filters
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a specific task
- `DELETE /tasks/{id}` - Delete a specific task
- `PATCH /tasks/{id}/complete` - Toggle task completion

## Environment Variables

**Backend (.env)**:
- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgresql://user:password@localhost/dbname`)

## Development Workflow

1. Start backend: `uvicorn main:app --reload`
2. In a new terminal, start frontend: `npm run dev`
3. Access the application at `http://localhost:3000`
4. The frontend will proxy API requests to the backend automatically