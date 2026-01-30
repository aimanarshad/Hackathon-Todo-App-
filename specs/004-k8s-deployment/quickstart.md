# Quickstart: Kubernetes Containerized Deployment

## Prerequisites

Before deploying the Todo application to Kubernetes, ensure you have the following installed:

- **Docker** (v20.10 or higher)
- **Minikube** (v1.28 or higher)
- **Helm** (v3.10 or higher)
- **kubectl** (v1.25 or higher)
- **Node.js** (v18 or higher) - for local development
- **Python** (v3.13 or higher) - for backend development

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Start Minikube Cluster
```bash
minikube start --driver=docker
```

### 3. Build Docker Images
There are two approaches to build the Docker images:

#### Using Gordon (AI-Assisted)
```bash
# If Gordon is available
gordon build -f docker/Dockerfile.frontend -t todo-frontend:latest .
gordon build -f docker/Dockerfile.backend -t todo-backend:latest .
```

#### Using Standard Docker Commands
```bash
# If Gordon is not available
docker build -f docker/Dockerfile.frontend -t todo-frontend:latest .
docker build -f docker/Dockerfile.backend -t todo-backend:latest .
```

### 4. Load Images into Minikube
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 5. Configure Database Connection
Ensure your Neon PostgreSQL connection string is available. You can either:

- Set it in your local `.env` file and it will be referenced during deployment
- Modify the `charts/todo-app/values.yaml` file with your database connection string

### 6. Deploy with Helm
```bash
# Navigate to the charts directory
cd charts

# Install the Helm chart
helm install todo-app todo-app/ --values todo-app/values.yaml
```

### 7. Verify Deployment
```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# Check if everything is working
kubectl get all
```

### 8. Access the Application
```bash
# Get the frontend service URL
minikube service todo-frontend-service --url

# Or use the ingress if configured
minikube tunnel  # In a separate terminal
# Then access http://localhost
```

## Deployment Commands Reference

### Common Helm Commands
```bash
# Upgrade the deployment
helm upgrade todo-app todo-app/ --values todo-app/values.yaml

# Uninstall the deployment
helm uninstall todo-app

# Check deployment status
helm status todo-app

# List all releases
helm list
```

### Common Kubernetes Commands
```bash
# Check pod status
kubectl get pods

# Check logs of frontend pod
kubectl logs -l app=todo-frontend

# Check logs of backend pod
kubectl logs -l app=todo-backend

# Port forward for debugging
kubectl port-forward svc/todo-frontend-service 3000:80
kubectl port-forward svc/todo-backend-service 8000:80

# Describe deployment for troubleshooting
kubectl describe deployment todo-frontend-deployment
kubectl describe deployment todo-backend-deployment
```

### Local Development vs. Kubernetes
While the application is deployed to Kubernetes, you can still develop locally:

```bash
# Run frontend locally
cd frontend
npm install
npm run dev

# Run backend locally
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure you've loaded images into minikube with `minikube image load`

2. **Database connection failures**: Verify your Neon PostgreSQL connection string is correct and accessible

3. **Service not accessible**: Check that the ingress controller is running in minikube:
   ```bash
   minikube addons enable ingress
   ```

4. **Resource constraints**: Adjust resource limits in `values.yaml` if pods are being evicted

### Debugging Steps
1. Check pod status: `kubectl get pods`
2. Examine pod logs: `kubectl logs <pod-name>`
3. Describe pod for details: `kubectl describe pod <pod-name>`
4. Check events: `kubectl get events --sort-by=.metadata.creationTimestamp`

## Cleanup

To remove the deployment and stop minikube:

```bash
# Uninstall the Helm release
helm uninstall todo-app

# Stop minikube
minikube stop

# Optionally delete the cluster
minikube delete
```