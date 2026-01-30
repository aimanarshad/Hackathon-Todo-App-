# Quickstart Guide: Phase 5 Advanced Cloud Deployment

## Overview

This guide provides instructions for setting up, developing, and deploying the Phase 5 Advanced Cloud Deployment features including recurring tasks, due date reminders, event-driven architecture with Kafka, and Dapr integration.

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube for local development, OKE for cloud)
- Dapr CLI and runtime
- kubectl
- Helm 3+
- Python 3.13+ with uv
- Node.js 20+ with pnpm
- Oracle Cloud account (for OKE deployment)
- GitHub account (for CI/CD)

## Local Development Setup

### 1. Clone and Initialize the Repository

```bash
git clone <repository-url>
cd hackathon-todo
uv venv
source .venv/bin/activate
uv pip sync backend/requirements-dev.txt
cd frontend
pnpm install
```

### 2. Start Dapr Locally

```bash
# Install Dapr
dapr init

# Start Dapr with the configuration for Phase 5
dapr run --config ./dapr/config.yaml --components-path ./dapr/components
```

### 3. Set Up Local Kafka (for event-driven features)

For local development, you can use Docker to run Kafka:

```bash
# Start Kafka using the provided docker-compose
cd kafka/local
docker-compose up -d
```

### 4. Run the Application Locally

```bash
# Terminal 1: Start the backend with Dapr
cd backend
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 -- python src/main.py

# Terminal 2: Start the frontend
cd frontend
pnpm dev
```

## Dapr Components Configuration

The Phase 5 implementation uses several Dapr components:

### Pub/Sub Component (Kafka)
Located at: `dapr/components/pubsub.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092"
  - name: consumerGroup
    value: "todo-app"
```

### State Store Component (PostgreSQL)
Located at: `dapr/components/statestore.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://username:password@localhost:5432/todo_db"
```

### Secret Store Component
Located at: `dapr/components/secretstore.yaml`

```yaml
api FIXME: Complete secret store configuration
```

## Developing Recurring Tasks Feature

### Backend Implementation

The recurring tasks functionality is located in `backend/src/tasks/recurrence_engine.py`:

```python
# Example of creating a recurring task
from backend.src.tasks.recurrence_engine import RecurrenceEngine

engine = RecurrenceEngine()
await engine.create_recurring_task(
    content="Daily standup meeting",
    pattern_type="daily",
    interval=1,
    start_date=datetime.now(),
    end_date=datetime(2024, 12, 31)
)
```

### API Endpoints

New endpoints for recurring tasks:
- `POST /api/v1/tasks/recurring` - Create recurring task
- `GET /api/v1/tasks/recurring/{task_id}` - Get recurring task details
- `PUT /api/v1/tasks/recurring/{task_id}` - Update recurring task
- `DELETE /api/v1/tasks/recurring/{task_id}` - Delete recurring task pattern

## Developing Due Date Reminders Feature

### Reminder Engine

The reminder functionality is implemented in `backend/src/tasks/reminder_engine.py`:

```python
# Schedule a reminder
from backend.src.tasks.reminder_engine import ReminderEngine

engine = ReminderEngine()
await engine.schedule_reminder(
    task_id=123,
    due_date=datetime(2024, 1, 1, 10, 0),
    reminder_offset_hours=24  # Send reminder 24 hours before due
)
```

### Event Processing

Events are processed through Kafka consumers in `kafka/consumers/reminder_consumer.py`:

```python
async def process_reminder_event(event_data: dict):
    # Handle reminder events from Kafka
    task_id = event_data['task_id']
    # Send reminder notification
    await send_notification(task_id)
```

## Deploying to Minikube (Local K8s)

### 1. Start Minikube

```bash
minikube start
minikube addons enable ingress
```

### 2. Install Dapr on Minikube

```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait
```

### 3. Deploy Application

```bash
# Build and push local images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Load images into minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Deploy using Helm
helm upgrade --install todo-app ./charts/todo-app \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest \
  --set dapr.enabled=true
```

## Deploying to Oracle OKE (Cloud)

### 1. Set Up Oracle Cloud CLI

```bash
# Install OCI CLI
curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh -o install.sh
bash install.sh

# Configure OCI CLI
oci setup config
```

### 2. Create OKE Cluster

```bash
# Create a cluster using the provided script
./scripts/deploy-oke.sh create-cluster
```

### 3. Deploy Application to OKE

```bash
# Get cluster credentials
oci ce cluster create-kubeconfig --cluster-id <cluster-id> --file $HOME/.kube/config --region us-sanjose-1

# Install Dapr on OKE
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

# Deploy application
helm upgrade --install todo-app ./charts/todo-app \
  --set backend.image.repository=<container-registry>/todo-backend \
  --set frontend.image.repository=<container-registry>/todo-frontend \
  --set dapr.enabled=true
```

## CI/CD Pipeline Setup

### GitHub Actions Workflow

The CI/CD pipeline is configured in `.github/workflows/deploy-oke.yml`:

```yaml
name: Deploy to OKE
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Build and Push Images
      run: |
        docker build -t todo-backend:${{ github.sha }} ./backend
        docker push <registry>/todo-backend:${{ github.sha }}

    - name: Deploy to OKE
      run: |
        # Deploy using Helm with new image tag
        helm upgrade --install todo-app ./charts/todo-app \
          --set backend.image.tag=${{ github.sha }}
```

### Setting Up Secrets in GitHub

Add the following secrets to your GitHub repository:
- `OCI_CONFIG` - Base64 encoded OCI config file
- `OCI_PRIVATE_KEY` - Base64 encoded OCI private key
- `CONTAINER_REGISTRY` - Oracle Cloud Container Registry URL

## Testing the Event-Driven Architecture

### Producing Events

```python
# Publish task event using Dapr
import requests

dapr_url = "http://localhost:3500/v1.0/publish/pubsub/task-events"
event_data = {
    "event_type": "task_created",
    "task_id": 123,
    "timestamp": "2024-01-01T10:00:00Z",
    "payload": {"content": "New task"}
}

requests.post(dapr_url, json=event_data)
```

### Consuming Events

Kafka consumers are implemented as separate services that listen to specific topics:

```python
# Consumer service that listens to reminder events
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'reminders',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    handle_reminder_event(message.value)
```

## Monitoring and Observability

### Accessing Dashboards

- Prometheus: http://localhost:9090 (local) or via OKE ingress
- Grafana: http://localhost:3000 (local) or via OKE ingress
- Dapr Dashboard: `dapr dashboard` command

### Key Metrics to Monitor

- Task processing rate
- Reminder delivery success rate
- Kafka topic lag
- Dapr sidecar health
- Database connection pool usage

## Troubleshooting

### Common Issues

1. **Dapr Sidecars Not Starting**
   - Check if Dapr runtime is installed: `dapr status -k`
   - Verify component configurations have no syntax errors

2. **Kafka Connection Issues**
   - Ensure Kafka brokers are running and accessible
   - Check network connectivity between services

3. **Database Connection Problems**
   - Verify PostgreSQL is accessible
   - Check connection string in Dapr state component

4. **Helm Deployment Failures**
   - Ensure all required values are set
   - Check for resource limits in the cluster

### Debugging Commands

```bash
# Check Dapr sidecars
kubectl get pods -l app=todo-backend
kubectl logs <pod-name> -c daprd

# Check Kafka topics
kubectl exec -it <kafka-pod> -- kafka-topics.sh --list --bootstrap-server localhost:9092

# Check application logs
kubectl logs -f deployment/todo-backend
```

## Next Steps

1. Scale the application based on demand
2. Enhance monitoring with custom dashboards
3. Implement advanced analytics for task patterns
4. Add more notification channels for reminders
5. Optimize performance for large datasets

## Completed Features

All Phase 5 features have been implemented:
- ✅ Recurring Tasks Management (daily, weekly, monthly patterns)
- ✅ Due Date Reminders with multiple notification methods
- ✅ Event-Driven Architecture with Kafka and Dapr Pub/Sub
- ✅ Cloud Deployment to Oracle OKE with CI/CD pipeline
- ✅ Monitoring and Observability with Prometheus and Grafana
- ✅ Frontend Integration with dedicated UI components
- ✅ Database migrations and state management
- ✅ Security hardening and health checks