# Implementation Plan: Kubernetes Containerized Deployment

**Branch**: `004-k8s-deployment` | **Date**: 2026-01-21 | **Spec**: [Kubernetes Containerized Deployment](./spec.md)
**Input**: Feature specification from `/specs/004-k8s-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Containerize the existing Todo application (frontend Next.js + backend FastAPI) with Docker, package deployment using Helm charts, and deploy to a local Minikube Kubernetes cluster. The solution will include Dockerfiles for both frontend and backend, Helm charts with deployments and services, and deployment automation using kubectl-ai/kagent commands while maintaining compatibility with existing Phase 1-3 functionality.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend), Node.js 20+
**Primary Dependencies**: Docker, Kubernetes (Minikube), Helm, FastAPI, Next.js, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL (existing from Phase 2-3)
**Testing**: kubectl commands, Helm lint/test, Docker validation
**Target Platform**: Local Minikube Kubernetes cluster
**Project Type**: Containerized web application
**Performance Goals**: Sub-second pod startup times, minimal resource overhead for local development
**Constraints**: Must not modify existing Phase 1-3 code, maintain backward compatibility with local development workflow
**Scale/Scope**: Local development environment supporting frontend + backend + database connectivity

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Compliance Verification (Pre-Design)**:
- ✅ **Spec-Driven Development**: All code (Dockerfiles, Helm charts, deployment scripts) will be generated from refined specifications
- ✅ **Backward Compatibility**: No modifications to existing Phase 1-3 code; only new files/folders will be added
- ✅ **Monorepo Structure**: Following prescribed structure with new docker/, charts/, k8s/ folders
- ✅ **Preservation Rule**: All existing functionality from Phases 1-3 remains intact
- ✅ **Phase 4 Requirements**: Containerization, Helm packaging, Minikube deployment as specified

**Constitution Compliance Verification (Post-Design)**:
- ✅ **Spec-Driven Development**: Dockerfiles, Helm charts, and deployment scripts will follow specification requirements
- ✅ **Backward Compatibility**: Design preserves all existing Phase 1-3 functionality with no modifications
- ✅ **Monorepo Structure**: Confirmed new directories docker/, charts/, k8s/ align with constitution requirements
- ✅ **Preservation Rule**: Data model and contracts respect existing Phase 2-3 database schema
- ✅ **Phase 4 Requirements**: Containerization approach, Helm structure, and Minikube deployment meet specification

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
hackathon-todo/
├── frontend/                    # Phase 2 & 3: Next.js app (untouched)
├── backend/                     # Phase 2 & 3: FastAPI app (untouched)
│   ├── agents/                  # Phase 3: Gemini + LangChain
│   ├── mcp/                     # Phase 3: MCP tools
│   ├── routers/                 # Phase 2 & 3: tasks.py + chat.py
│   ├── conversation_models.py   # Phase 3
│   └── ...                      # All Phase 2 & 3 files preserved
├── specs/                       # All phases' specs
├── src/                         # Phase 1 console code (historical)
├── docker/                      # NEW: Dockerfiles for frontend/backend
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── .dockerignore
├── charts/                      # NEW: Helm charts
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment-frontend.yaml
│           ├── deployment-backend.yaml
│           ├── service-frontend.yaml
│           ├── service-backend.yaml
│           ├── ingress.yaml
│           └── configmap.yaml
├── k8s/                         # NEW: Kubernetes manifests/commands
│   ├── minikube-setup.sh
│   ├── deploy.sh
│   └── commands.md
├── .specify/                    # Spec-Kit Plus memory/templates
├── CLAUDE.md                    # Prompt guidelines
├── README.md                    # Updated run/deploy instructions
└── .env                         # Local secrets (never commit)
```

**Structure Decision**: Following the web application structure as the feature involves frontend (Next.js) and backend (FastAPI) components that need to be containerized and deployed to Kubernetes. New directories docker/, charts/, and k8s/ are created per Phase 4 requirements while preserving all existing Phase 1-3 code.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New folder structure | Phase 4 requirements mandate docker/, charts/, k8s/ directories | Existing structure doesn't support containerization and orchestration |
| Dependency on external tools | Kubernetes deployment requires Docker, Helm, Minikube | Local development workflow needs containerization for consistency |
