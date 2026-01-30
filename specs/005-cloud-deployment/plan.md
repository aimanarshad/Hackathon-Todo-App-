# Implementation Plan: Phase 5 Advanced Cloud Deployment

**Branch**: `005-cloud-deployment` | **Date**: 2026-01-27 | **Spec**: [specs/005-cloud-deployment/spec.md](specs/005-cloud-deployment/spec.md)
**Input**: Feature specification from `/specs/005-cloud-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of advanced cloud-native features including recurring tasks (daily/weekly), due date reminders using Dapr Jobs, event-driven architecture with Kafka, and deployment to Oracle OKE with CI/CD pipeline. The solution extends existing Todo application with Dapr for distributed runtime patterns (Pub/Sub, State, Jobs, Secrets) while maintaining backward compatibility with all previous phases.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend), Node.js 20+ (build tools)
**Primary Dependencies**: FastAPI, SQLModel, Next.js 14+, Dapr, Kafka/Redpanda, kubectl, Helm, Docker, GitHub Actions
**Storage**: Neon Serverless PostgreSQL (via Dapr State component)
**Testing**: pytest (backend), Jest/React Testing Library (frontend), kubectl for K8s integration tests
**Target Platform**: Oracle OKE (Oracle Kubernetes Engine), with local Minikube for development
**Project Type**: Web application (full-stack with frontend, backend, and infrastructure)
**Performance Goals**: Support 1000+ concurrent users, <2 second response times, 99% uptime, 10,000+ task events/hour processing
**Constraints**: Maintain backward compatibility with Phases 1-4, zero-downtime deployments, secure secret management
**Scale/Scope**: Support enterprise-scale deployments with auto-scaling, monitoring, and observability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven Development**: All code (application logic, infrastructure, Dockerfiles, Helm charts, Dapr components, CI/CD workflows) must be generated from this plan - ✅ COMPLIANT
2. **Iterative Evolution & Backward Compatibility**: All features and code from previous phases must remain functional - ✅ COMPLIANT
3. **Clean Architecture & Separation of Concerns**: Layering maintained - presentation (frontend), business logic (backend), data (PostgreSQL), orchestration (K8s), event-driven (Kafka + Dapr) - ✅ COMPLIANT
4. **Preservation Rule**: No deletion/modification of files from Phases 1-4 - ✅ COMPLIANT
5. **Monorepo Structure**: All additions stay within one repository with clear organization - ✅ COMPLIANT

*Post-Design Constitution Check: All gates still compliant after Phase 1 design work.*

## Project Structure

### Documentation (this feature)

```text
specs/005-cloud-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (existing from previous phases)
backend/
├── src/
│   ├── models/          # SQLModel models (existing from Phase 2)
│   ├── services/        # Business logic (existing from Phase 2)
│   ├── api/             # FastAPI endpoints (existing from Phase 2)
│   ├── dapr/            # New Dapr integration services
│   └── tasks/           # New recurring tasks and job scheduling logic
└── tests/

frontend/
├── src/
│   ├── components/      # React components (existing from Phase 2)
│   ├── pages/           # Next.js pages (existing from Phase 2)
│   └── services/        # API clients (existing from Phase 2)
└── tests/

# Infrastructure and deployment (new for Phase 5)
docker/
├── backend/Dockerfile
├── frontend/Dockerfile
└── docker-compose.yml

charts/                  # Helm charts (existing from Phase 4, extended)
├── todo-app/
│   ├── templates/
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── dapr-components/
│   │   │   ├── pubsub-kafka.yaml
│   │   │   ├── statestore-postgres.yaml
│   │   │   ├── jobs.yaml
│   │   │   └── secretstore.yaml
│   │   └── kafka/
│   │       ├── kafka-cluster.yaml
│   │       └── kafka-topic.yaml
│   ├── Chart.yaml
│   └── values.yaml

dapr/
├── components/
│   ├── pubsub.yaml      # Kafka pub/sub component
│   ├── statestore.yaml  # PostgreSQL state store component
│   ├── jobs.yaml        # Dapr jobs component
│   └── secretstore.yaml # Secret store component
└── config.yaml

kafka/
├── topics/
│   ├── task-events.yaml
│   ├── reminders.yaml
│   └── task-updates.yaml
└── consumers/

.github/
└── workflows/
    └── deploy-oke.yml   # GitHub Actions CI/CD workflow

monitoring/
├── prometheus/
│   └── prometheus.yml
└── grafana/
    └── dashboards/
        └── todo-app.json

scripts/
├── deploy-oke.sh        # Oracle OKE deployment script
├── setup-kafka.sh       # Kafka setup script
└── setup-dapr.sh        # Dapr setup script
```

**Structure Decision**: The existing web application structure from previous phases is extended with new directories for Dapr integration, Kafka event processing, cloud deployment configurations, and monitoring. The structure maintains backward compatibility while adding cloud-native capabilities.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional infrastructure layers (Dapr, Kafka) | Required for event-driven architecture and advanced cloud features | Simpler in-process job scheduling would not scale or provide the required cloud-native capabilities |
| Multiple deployment environments (local, minikube, OKE) | Required for development workflow while supporting cloud deployment | Single environment approach would not allow for proper development/testing before cloud deployment |
