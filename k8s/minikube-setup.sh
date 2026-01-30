#!/bin/bash

# Minikube setup script for Todo App deployment

set -e  # Exit on any error

echo "Setting up Minikube for Todo App deployment..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Error: minikube is not installed"
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed"
    exit 1
fi

# Start minikube with recommended resources
echo "Starting Minikube with 4 CPUs and 8GB memory..."
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=docker

# Enable ingress addon
echo "Enabling ingress addon..."
minikube addons enable ingress

# Verify cluster is ready
echo "Verifying cluster status..."
kubectl cluster-info
kubectl get nodes

echo "Minikube setup completed successfully!"
echo "You can now build Docker images and deploy the application."