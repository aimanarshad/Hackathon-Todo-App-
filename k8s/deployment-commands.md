# Kubernetes Deployment Commands for Todo App

This document contains the kubectl commands and deployment procedures for the Todo application on Minikube using Helm.

## Prerequisites

Before deploying, ensure you have:

- Docker installed and running
- Minikube installed and running (`minikube start`)
- Helm installed
- kubectl installed and configured to connect to your Minikube cluster

## Minikube Setup

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Enable ingress addon for external access (optional)
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Docker Image Building and Loading

### Build Docker Images

```bash
# Build frontend image
docker build -f docker/Dockerfile.frontend -t todo-frontend:latest .

# Build backend image
docker build -f docker/Dockerfile.backend -t todo-backend:latest .
```

### Load Images into Minikube

```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest
```

## Helm Chart Deployment

### Install the Chart

```bash
# Navigate to charts directory
cd charts

# Install the chart with default values
helm install todo-app todo-app/ --values todo-app/values.yaml

# Install with custom values (e.g., database connection)
helm install todo-app todo-app/ --set backend.databaseUrl="your-neon-db-connection-string"
```

### Upgrade the Chart

```bash
# Upgrade the release with new values
helm upgrade todo-app todo-app/ --values todo-app/values.yaml

# Upgrade with specific database URL
helm upgrade todo-app todo-app/ --set backend.databaseUrl="your-neon-db-connection-string"
```

### Check Deployment Status

```bash
# Check all resources
kubectl get all

# Check pods specifically
kubectl get pods

# Check services
kubectl get services

# Check deployments
kubectl get deployments

# Check the status of your Helm release
helm status todo-app
```

## Service Access

### Get Service URLs

```bash
# Get frontend service URL
minikube service todo-app-frontend-service --url

# Get backend service URL
minikube service todo-app-backend-service --url
```

### Port Forwarding (Alternative Access Method)

```bash
# Port forward frontend service
kubectl port-forward svc/todo-app-frontend-service 3000:80

# Port forward backend service
kubectl port-forward svc/todo-app-backend-service 8000:80
```

## Monitoring and Logging

### Check Pod Logs

```bash
# Get frontend pod logs
kubectl logs -l app=todo-frontend

# Get backend pod logs
kubectl logs -l app=todo-backend

# Follow logs in real-time
kubectl logs -l app=todo-frontend -f
kubectl logs -l app=todo-backend -f
```

### Describe Resources for Debugging

```bash
# Describe frontend deployment
kubectl describe deployment todo-app-frontend

# Describe backend deployment
kubectl describe deployment todo-app-backend

# Describe services
kubectl describe service todo-app-frontend-service
kubectl describe service todo-app-backend-service
```

## Health Checks

### Verify Pod Status

```bash
# Check if pods are running
kubectl get pods -o wide

# Check if pods are ready
kubectl wait --for=condition=Ready pod -l app=todo-frontend
kubectl wait --for=condition=Ready pod -l app=todo-backend
```

### Check Health Endpoints

```bash
# Exec into frontend pod and check health
kubectl exec -it $(kubectl get pods -l app=todo-frontend -o jsonpath='{.items[0].metadata.name}') -- curl localhost:3000/

# Exec into backend pod and check health
kubectl exec -it $(kubectl get pods -l app=todo-backend -o jsonpath='{.items[0].metadata.name}') -- curl localhost:8000/health
```

## Troubleshooting

### Common Issues and Solutions

```bash
# Check events for issues
kubectl get events --sort-by='.lastTimestamp'

# Check if there are resource constraints
kubectl top nodes
kubectl top pods

# Check if ingress is working (if enabled)
kubectl get ingress

# Check ConfigMap values
kubectl get configmap todo-app-config -o yaml
```

### Restart Deployments

```bash
# Restart frontend deployment
kubectl rollout restart deployment/todo-app-frontend

# Restart backend deployment
kubectl rollout restart deployment/todo-app-backend

# Check rollout status
kubectl rollout status deployment/todo-app-frontend
kubectl rollout status deployment/todo-app-backend
```

## Uninstall

```bash
# Uninstall the Helm release
helm uninstall todo-app

# Verify deletion
kubectl get all
```

## Automation Scripts

For automated deployment, you can create shell scripts with these commands. The following is an example of what could be in `k8s/deploy.sh`:

```bash
#!/bin/bash

# Load images into minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Install or upgrade the Helm chart
if helm status todo-app; then
    echo "Upgrading existing release..."
    helm upgrade todo-app charts/todo-app/ --values charts/todo-app/values.yaml
else
    echo "Installing new release..."
    helm install todo-app charts/todo-app/ --values charts/todo-app/values.yaml
fi

# Wait for deployments to be ready
kubectl wait --for=condition=Ready pods -l app=todo-frontend --timeout=300s
kubectl wait --for=condition=Ready pods -l app=todo-backend --timeout=300s

echo "Deployment completed!"
```

## Gordon Integration Commands (if available)

```bash
# If Gordon is available for Docker operations
gordon build -f docker/Dockerfile.frontend -t todo-frontend:latest .
gordon build -f docker/Dockerfile.backend -t todo-backend:latest .

# Fallback to standard Docker commands if Gordon is not available
docker build -f docker/Dockerfile.frontend -t todo-frontend:latest .
docker build -f docker/Dockerfile.backend -t todo-backend:latest .
```