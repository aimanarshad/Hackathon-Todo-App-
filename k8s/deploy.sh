#!/bin/bash

# Deployment script for Todo App to Minikube using Helm

set -e  # Exit on any error

echo "Starting deployment of Todo App to Minikube..."

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "Error: Minikube is not running. Please start it with 'minikube start'."
    exit 1
fi

# Build Docker images
echo "Building Docker images..."
docker build -f docker/Dockerfile.frontend -t todo-frontend:latest .
docker build -f docker/Dockerfile.backend -t todo-backend:latest .

# Load images into minikube
echo "Loading images into Minikube..."
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Check if Helm release exists
if helm status todo-app &> /dev/null; then
    echo "Upgrading existing release..."
    helm upgrade todo-app charts/todo-app/ --values charts/todo-app/values.yaml
else
    echo "Installing new release..."
    helm install todo-app charts/todo-app/ --values charts/todo-app/values.yaml
fi

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=Ready pods -l app=todo-frontend --timeout=300s
kubectl wait --for=condition=Ready pods -l app=todo-backend --timeout=300s

# Verify deployment
echo "Verifying deployment..."
kubectl get pods
kubectl get services
kubectl get deployments

echo "Deployment completed successfully!"

# Show service URLs if available
echo "Service URLs:"
minikube service todo-app-frontend-service --url || echo "Frontend service not available via minikube service"
minikube service todo-app-backend-service --url || echo "Backend service not available via minikube service"

echo "Application deployed and ready!"