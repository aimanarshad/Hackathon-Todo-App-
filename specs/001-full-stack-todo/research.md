# Research Notes: Phase 2 Full-Stack Todo Web App

## Decision: Technology Stack Selection
**Rationale**: Selected FastAPI + SQLModel for backend and Next.js + TypeScript + Tailwind for frontend based on constitution requirements and industry best practices for full-stack web applications.

**Alternatives considered**:
- Backend: Django vs FastAPI - Chose FastAPI for better performance and modern async support
- Frontend: React + Vite vs Next.js - Chose Next.js for built-in routing and SSR capabilities
- Database: SQLite vs PostgreSQL - Chose PostgreSQL for production readiness and Neon compatibility

## Decision: Project Structure
**Rationale**: Monorepo with separate backend/ and frontend/ directories to maintain clean separation of concerns while keeping the codebase manageable.

**Alternatives considered**:
- Single repository with mixed code - rejected for maintainability
- Separate repositories - rejected for complexity in deployment and coordination

## Decision: API Design Pattern
**Rationale**: RESTful API with standard HTTP methods following the specification requirements for CRUD operations plus PATCH for toggling completion status.

**Alternatives considered**:
- GraphQL API - rejected for simplicity as REST meets all requirements
- RPC-style API - rejected for not following standard conventions

## Decision: Data Model Implementation
**Rationale**: Using SQLModel which combines SQLAlchemy and Pydantic for type safety and ORM capabilities, matching the specification requirements.

**Alternatives considered**:
- Pure SQLAlchemy - rejected for less type safety
- Tortoise ORM - rejected for less compatibility with FastAPI ecosystem
- Raw SQL - rejected for lack of ORM benefits

## Decision: Authentication Strategy
**Rationale**: No authentication for Phase 2 as specified, but designing with user_id field ready for future implementation in Phase 3.

**Alternatives considered**:
- Implement basic auth now - rejected as not required for Phase 2
- JWT tokens - rejected as not required for Phase 2