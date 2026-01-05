# Research: Todo In-Memory Python Console App

## Decision: Single-file application architecture
**Rationale**: Following the constitution principle of simplicity, a single-file approach (main.py) is chosen to implement all functionality. This keeps the codebase simple and easy to understand while meeting all requirements.
**Alternatives considered**:
- Multi-file modular approach with separate modules for each feature
- Object-oriented approach with Task class and TodoApp class

## Decision: Python standard libraries only
**Rationale**: The specification calls for standard libs only, and the requirements can be met without external dependencies. This keeps the project lightweight and reduces complexity.
**Alternatives considered**:
- Using external libraries for CLI handling (like click)
- Using external libraries for data validation

## Decision: In-memory storage using global list
**Rationale**: The specification explicitly states "no persistence", so a simple in-memory list is appropriate. This meets the requirement while keeping implementation simple.
**Alternatives considered**:
- Using a dictionary with ID as key for faster lookups
- Using a class-based approach to encapsulate the task list

## Decision: Menu-driven interface with numbered options
**Rationale**: The specification explicitly calls for a menu-driven loop (1-6 options including Exit), which provides a clear and simple user interface.
**Alternatives considered**:
- Command-line argument based interface
- Interactive prompt for each operation

## Decision: Task data model as dictionary
**Rationale**: The specification defines the data model as {'id': int, 'title': str, 'description': str, 'completed': bool}, which is simple and effective for this use case.
**Alternatives considered**:
- Using a named tuple
- Using a dataclass
- Using a custom class