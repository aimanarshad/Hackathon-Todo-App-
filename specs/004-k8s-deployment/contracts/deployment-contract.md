# API Contract: Kubernetes Deployment Configuration

## Purpose
This document defines the contract for deploying the Todo application to Kubernetes, including the expected configurations, interfaces, and behaviors for the containerized applications.

## Deployment Configuration Contract

### Frontend Service Contract
- **Service Name**: `todo-frontend-service`
- **Port**: 80 (internal), mapped to container port 3000
- **Environment Variables Expected**:
  - `NEXT_PUBLIC_API_URL`: URL of the backend API service
  - `NODE_ENV`: Environment mode (production/development)
- **Health Check Endpoint**: `/health` or `/` with 200 OK response
- **Resource Requirements**:
  - CPU: minimum 100m, limit 500m
  - Memory: minimum 128Mi, limit 512Mi

### Backend Service Contract
- **Service Name**: `todo-backend-service`
- **Port**: 80 (internal), mapped to container port 8000
- **Environment Variables Expected**:
  - `DATABASE_URL`: PostgreSQL connection string
  - `ENVIRONMENT`: Environment mode (production/development)
  - `SERVER_HOST`: Host binding (should be 0.0.0.0 in container)
  - `SERVER_PORT`: Port binding (should be 8000 in container)
- **Health Check Endpoint**: `/health` or `/docs` with 200 OK response
- **Resource Requirements**:
  - CPU: minimum 100m, limit 1Gi
  - Memory: minimum 256Mi, limit 2Gi

## Container Interface Contract

### Frontend Container Interface
- **Exposed Port**: 3000
- **Working Directory**: `/app` (or equivalent)
- **Start Command**: `npm start` or equivalent production command
- **Expected Files**: Built Next.js application in container
- **Network Access**: Must be able to reach backend service

### Backend Container Interface
- **Exposed Port**: 8000
- **Working Directory**: `/app` (or equivalent)
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Expected Files**: Python application with dependencies installed
- **Network Access**: Must be able to reach PostgreSQL database

## Database Connection Contract
- **Connection Method**: Via environment variable `DATABASE_URL`
- **Protocol**: PostgreSQL wire protocol
- **Required Permissions**: Read/write access to todo application tables
- **Connection Pooling**: Application should implement appropriate pooling
- **SSL Mode**: Should support SSL connections (particularly for Neon)

## Kubernetes Resource Contract

### Deployment Requirements
- **Replicas**: Minimum 1 for local development
- **Selectors**: Must match service selectors
- **Labels**: Consistent labels for identification
- **Rolling Updates**: Support for rolling update deployments

### Service Requirements
- **Type**: ClusterIP for internal communication, LoadBalancer or NodePort for external access
- **Selectors**: Must match deployment pod selectors
- **Ports**: Correct port mapping between service and container ports

### Health Check Contract
- **Readiness Probe**: Determines when container can receive traffic
- **Liveness Probe**: Determines when container needs restart
- **Failure Threshold**: Reasonable thresholds to prevent flapping
- **Initial Delay**: Appropriate delays for application startup

## Configuration Management Contract

### ConfigMap Contract
- **Format**: Key-value pairs in Kubernetes ConfigMap format
- **Naming Convention**: Descriptive names that indicate purpose
- **Access Method**: Environment variables or mounted volumes

### Secret Contract
- **Sensitive Data**: Database credentials and API keys
- **Encoding**: Base64 encoded values
- **Access Method**: Environment variables or mounted files

## Network Contract

### Internal Communication
- **Frontend to Backend**: Must be able to reach backend service
- **Backend to Database**: Must be able to reach PostgreSQL
- **Service Discovery**: Through Kubernetes DNS resolution

### External Access
- **Ingress**: Should support external access via ingress controller
- **Load Balancer**: Should support external access via service
- **Security**: Appropriate network policies if required

## Security Contract

### Container Security
- **User**: Should run as non-root user when possible
- **Capabilities**: Minimal required capabilities
- **Privileges**: Non-privileged containers

### Network Security
- **TLS**: Support for encrypted communication
- **Authentication**: Appropriate authentication between services
- **Authorization**: Appropriate authorization for database access