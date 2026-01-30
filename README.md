# Phase 5 Advanced Cloud Deployment - Todo Web App

This project implements a full-stack todo application with advanced cloud-native features using FastAPI backend, Next.js frontend, and distributed systems patterns. The solution includes recurring tasks, due date reminders, event-driven architecture with Kafka, and deployment to Oracle OKE.

## Features

- **Core Task Management**: Create, read, update, delete, and mark tasks as complete
- **Enhanced Features**: Priority levels (high/medium/low) and tags for better organization
- **Advanced Organization**: Search, filter, and sort functionality
- **Recurring Tasks**: Daily, weekly, monthly recurring task patterns with templates
- **Due Date Reminders**: Automated reminders with multiple notification methods (push, email, SMS)
- **Event-Driven Architecture**: Kafka-based pub/sub for asynchronous task processing
- **Dapr Integration**: Distributed Application Runtime for microservice patterns
- **Cloud Deployment**: Production-ready deployment to Oracle Kubernetes Engine (OKE)
- **Monitoring & Observability**: Prometheus and Grafana for metrics and dashboards
- **Responsive UI**: Works on desktop and mobile devices with tabbed interface
- **API-First**: Clean REST API with full CRUD operations

## Tech Stack

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS, Material UI
- **Database**: PostgreSQL (via Dapr State component)
- **Event Streaming**: Apache Kafka (via Dapr Pub/Sub)
- **Distributed Runtime**: Dapr (Pub/Sub, State, Jobs, Secrets)
- **Orchestration**: Kubernetes, Helm, Docker
- **CI/CD**: GitHub Actions
- **Cloud**: Oracle Kubernetes Engine (OKE)
- **Monitoring**: Prometheus, Grafana

## API Endpoints

- `GET /api/tasks` - List all tasks with optional filters and sorting
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status
- `POST /api/v1/recurring-tasks` - Create recurring task template
- `GET /api/v1/recurring-tasks/{id}` - Get recurring task template
- `PUT /api/v1/recurring-tasks/{id}` - Update recurring task template
- `DELETE /api/v1/recurring-tasks/{id}` - Delete recurring task template
- `POST /api/v1/reminders` - Create task reminder
- `GET /api/v1/reminders` - List reminders
- `DELETE /api/v1/reminders/{id}` - Delete reminder
- `GET /api/v1/events/stream` - Server-sent events for real-time updates

## Environment Variables

Create a `.env` file in the project root with:

```
DATABASE_URL=postgresql://user:password@localhost/todo_db
NEXT_PUBLIC_API_URL=http://localhost:8000/api
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001
KAFKA_BROKERS=kafka:9092
```

## Running the Application

### With Dapr (Recommended for Phase 5 features)

1. Navigate to the project root
2. Install Dapr: `dapr init`
3. Start the backend with Dapr: `dapr run --app-id todo-backend --app-port 8000 -- python backend/main.py`
4. Start the frontend: `cd frontend && npm run dev`
5. The web app will be available at `http://localhost:3000`

### Local Development Setup

#### Backend (API Server)
1. Navigate to the `backend` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server with Dapr: `dapr run --app-id todo-backend --app-port 8000 -- python main.py`
4. The API will be available at `http://localhost:8000` (Dapr proxy at `http://localhost:3500/v1.0/invoke/todo-backend/method/`)

#### Frontend (Web App)
1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. The web app will be available at `http://localhost:3000`

### Running with Docker Compose (Event-driven setup)
1. Start all services: `docker-compose -f docker/docker-compose.phase5.yml up -d`
2. This includes Kafka, Zookeeper, backend, frontend, and Dapr sidecars

## Database Setup

1. Ensure PostgreSQL is running (Neon DB recommended for cloud deployment)
2. Update the DATABASE_URL in your .env file
3. The database tables will be created automatically on startup
4. For Phase 5, run the migration: `python backend/migrations/add_phase5_fields.py`

## Dapr Configuration

The application uses Dapr for distributed services:
- Pub/Sub: Kafka for event-driven architecture
- State Management: PostgreSQL for task persistence
- Secrets: Secure storage for sensitive data
- Service Invocation: Inter-service communication

Components are configured in `dapr/components/` directory.

## Kafka and Event Processing

The event-driven architecture uses Apache Kafka:
- Topics: task-events, reminders, task-updates
- Producers: Backend services publish task events
- Consumers: Background services process events asynchronously
- Dapr handles the integration via pubsub component

## Cloud Deployment

The application is designed for deployment to Oracle Kubernetes Engine (OKE):
- Helm charts in `charts/todo-app/` for Kubernetes deployment
- CI/CD pipeline in `.github/workflows/deploy-oke.yml`
- Monitoring with Prometheus and Grafana
- Dapr sidecars for distributed services on Kubernetes

## Development

The application follows a spec-driven development approach. All code is generated from the specifications in the `specs/` directory.

## Phase 5 Features

### Recurring Tasks
- Create recurring tasks with daily, weekly, or monthly patterns
- Set recurrence intervals and end dates
- Manage recurring task templates
- Automatic generation of task instances

### Due Date Reminders
- Set due dates for tasks
- Enable automated reminders
- Choose reminder notification methods (push, email, SMS)
- Manage reminder settings per task

### Event-Driven Architecture
- Real-time task event processing
- Asynchronous operations with Kafka
- Decoupled services with Dapr
- Server-sent events for real-time UI updates

### Cloud-Native Deployment
- Containerized services with Docker
- Kubernetes orchestration with Helm
- Dapr for portable distributed applications
- CI/CD pipeline for automated deployment
# Todo-App
