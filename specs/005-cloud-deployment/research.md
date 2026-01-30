# Research Summary: Phase 5 Advanced Cloud Deployment

## Executive Summary

This research addresses the technical decisions required for implementing Phase 5 Advanced Cloud Deployment, focusing on recurring tasks, due date reminders, event-driven architecture with Kafka, Dapr integration, Oracle OKE deployment, and CI/CD pipeline.

## Decision: Dapr Jobs Component Implementation

**Rationale**: Dapr Jobs component is essential for scheduling recurring tasks and due date reminders. Since Dapr doesn't officially provide a "jobs" component, we'll implement a custom solution using Dapr Workflows or leverage Kubernetes CronJobs integrated with Dapr services.

**Alternatives considered**:
1. Native Kubernetes CronJobs - Provides native scheduling but less integration with Dapr state management
2. Custom scheduler service - More control but increases complexity
3. Third-party schedulers (Quartz.NET port, APScheduler) - Would require additional dependencies

**Chosen approach**: Combination of Dapr Workflows for recurring tasks and Kubernetes CronJobs for scheduled reminders, both interacting with Dapr state and pubsub components.

## Decision: Kafka Implementation Strategy

**Rationale**: Kafka is required for the event-driven architecture to handle task events, reminders, and updates. For cloud deployment, we need to decide between managed Kafka services and self-hosted solutions.

**Alternatives considered**:
1. Redpanda Cloud (managed) - Lower operational overhead, serverless scaling
2. Oracle Cloud Streaming (OKE native) - Better integration with Oracle infrastructure
3. Self-hosted Kafka on OKE (Strimzi) - Full control but higher operational complexity

**Chosen approach**: Redpanda Cloud for development and testing, with the ability to switch to self-hosted Strimzi Kafka on OKE for production scenarios.

## Decision: Oracle OKE Cluster Configuration

**Rationale**: Oracle OKE is the target Kubernetes platform for cloud deployment, offering an always-free tier suitable for development and small-scale production.

**Key considerations**:
- Node pool configuration (VM.Standard.E2.1.Micro for free tier)
- Network setup (VPC, load balancers)
- Integration with Neon PostgreSQL
- Dapr installation and configuration on the cluster

**Chosen approach**: Start with a minimal OKE cluster on Oracle's always-free tier, with horizontal pod autoscaling enabled for growth.

## Decision: Event Schema Design

**Rationale**: Standardized event schemas are needed for the Kafka topics to ensure interoperability between services.

**Design decisions**:
- task-events topic: Events for task creation, updates, completion, deletion
- reminders topic: Scheduled reminder triggers
- task-updates topic: Notifications for task changes

**Schema approach**: JSON-based events with common metadata (timestamp, correlation ID, causation ID) and specific payload structures for each event type.

## Decision: CI/CD Pipeline Architecture

**Rationale**: Automated CI/CD pipeline is required for continuous deployment to OKE.

**Components identified**:
- Build and test phases
- Docker image building and pushing to registry
- Helm chart versioning and deployment
- Health checks and rollback procedures

**Chosen approach**: GitHub Actions workflow with separate jobs for build/test, image push, and OKE deployment, with approval gates for production deployment.

## Decision: Monitoring and Observability Stack

**Rationale**: Proper monitoring is essential for a cloud-native application with distributed components.

**Components selected**:
- Prometheus for metrics collection
- Grafana for visualization
- Standard Dapr observability patterns
- Kubernetes-native monitoring

**Integration approach**: Pre-configured dashboards for application metrics, Dapr sidecar metrics, and Kubernetes infrastructure metrics.

## Decision: Recurring Task Implementation Strategy

**Rationale**: Need to implement recurring tasks that can be scheduled daily/weekly while maintaining data consistency.

**Technical approach**:
- Extend existing Task model with recurrence patterns
- Create a recurrence engine that generates new task instances
- Use Dapr state management for storing recurrence rules
- Leverage Dapr pubsub for triggering recurrence events

**Data model considerations**: Store recurrence patterns separately from individual task instances to avoid duplication.

## Decision: Due Date Reminder System

**Rationale**: Timely reminders are crucial for task management effectiveness.

**Technical approach**:
- Store due dates and reminder preferences in the task model
- Use Dapr Workflows or CronJobs to schedule reminders
- Implement reminder delivery via pubsub events
- Support configurable reminder timing (1 day before, 1 hour before, etc.)

## Security Considerations

**Secrets management**: Use Dapr secret store component to manage database credentials, API keys, and cloud provider credentials securely.

**Network security**: Implement proper network policies and service mesh patterns for inter-service communication.

**Authentication**: Maintain existing authentication patterns from previous phases while extending to new services.