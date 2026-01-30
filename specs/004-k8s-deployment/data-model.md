# Data Model: Kubernetes Containerized Deployment

## Container Configuration Entities

### Frontend Container Configuration
- **Image Name**: todo-frontend
- **Base Image**: node:20-alpine or node:20-slim depending on dependencies
- **Build Context**: ./frontend directory
- **Environment Variables**:
  - NEXT_PUBLIC_API_URL: URL for backend API
  - NODE_ENV: production or development
- **Ports**: 3000 (exposed port for Next.js)
- **Volumes**: None required for basic deployment
- **Health Check**: HTTP GET on /api/health or /

### Backend Container Configuration
- **Image Name**: todo-backend
- **Base Image**: python:3.13-slim
- **Build Context**: ./backend directory
- **Environment Variables**:
  - DATABASE_URL: Connection string for Neon PostgreSQL
  - ENVIRONMENT: production or development
  - SERVER_HOST: Host binding (0.0.0.0 for container)
  - SERVER_PORT: Port binding (8000 for FastAPI)
- **Ports**: 8000 (exposed port for FastAPI)
- **Volumes**: None required for basic deployment
- **Health Check**: HTTP GET on /health or /docs

## Kubernetes Resource Definitions

### Deployment Specifications
- **Frontend Deployment**:
  - replicas: 1 (for local development)
  - selector: app=todo-frontend
  - template: matching selector with frontend container
  - resource requests: CPU/Memory based on Next.js requirements
  - resource limits: Prevent resource exhaustion

- **Backend Deployment**:
  - replicas: 1 (for local development)
  - selector: app=todo-backend
  - template: matching selector with backend container
  - resource requests: CPU/Memory based on FastAPI requirements
  - resource limits: Prevent resource exhaustion

### Service Specifications
- **Frontend Service**:
  - type: ClusterIP or NodePort for local access
  - port: 80 (external access)
  - targetPort: 3000 (container port)
  - selector: app=todo-frontend

- **Backend Service**:
  - type: ClusterIP
  - port: 80 (external access)
  - targetPort: 8000 (container port)
  - selector: app=todo-backend

### ConfigMap Specifications
- **Application ConfigMap**:
  - NEXT_PUBLIC_API_URL: Backend service URL
  - ENVIRONMENT: production/development flags
  - Other non-sensitive configuration values

### Ingress Specifications
- **Main Ingress**:
  - host: localhost or local.minikube.host
  - paths: / for frontend, /api/* for backend
  - TLS: Optional for local development
  - loadBalancer: Depends on local setup

## Helm Values Structure

### Global Configuration
- **imageRegistry**: Registry for pulling images
- **imagePullSecrets**: Secrets for private registries
- **hostAliases**: Host mappings if needed

### Frontend Configuration
- **frontend.image.repository**: todo-frontend
- **frontend.image.tag**: latest or specific version
- **frontend.image.pullPolicy**: Always, IfNotPresent, or Never
- **frontend.service.type**: Service type (ClusterIP, NodePort)
- **frontend.service.port**: External port
- **frontend.resources**: Resource limits and requests
- **frontend.nodeSelector**: Node selection constraints
- **frontend.tolerations**: Taint tolerations
- **frontend.affinity**: Affinity settings

### Backend Configuration
- **backend.image.repository**: todo-backend
- **backend.image.tag**: latest or specific version
- **backend.image.pullPolicy**: Always, IfNotPresent, or Never
- **backend.service.type**: Service type (ClusterIP)
- **backend.service.port**: External port
- **backend.resources**: Resource limits and requests
- **backend.databaseUrl**: Neon PostgreSQL connection string
- **backend.nodeSelector**: Node selection constraints
- **backend.tolerations**: Taint tolerations
- **backend.affinity**: Affinity settings

## Deployment Process States

### Pre-deployment State
- Docker images built and available
- Minikube cluster running
- Helm initialized and ready

### Deployment State
- Helm chart installed
- Kubernetes resources created
- Pods running and healthy
- Services accessible

### Post-deployment State
- Ingress routes active
- Health checks passing
- Application accessible externally

## Validation Requirements

### Container Validation
- Images build successfully
- Images run without errors
- Health checks pass
- Environment variables properly loaded

### Kubernetes Validation
- Pods start successfully
- Services route traffic properly
- Ingress provides external access
- Resource limits respected

### Integration Validation
- Frontend can reach backend
- Backend can connect to database
- End-to-end functionality works
- Performance meets expectations