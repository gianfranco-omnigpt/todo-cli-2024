# CLI ToDo App

## GitHub Info
- owner: gianfranco-omnigpt
- repo: todo-cli-2024
- branch: main

## PRD (Product Requirements)

### Overview
A minimal command-line application for managing personal tasks.

### Problem
Users need a fast, lightweight way to track tasks without leaving the terminal.

### Target User
Developers and terminal-power users who prefer CLI tools.

### Core Features

| Feature | Description |
|---------|-------------|
| Add task | Create a new task with a description |
| List tasks | Display all tasks with status |
| Complete task | Mark a task as done |
| Delete task | Remove a task |

### User Stories
- As a user, I can add a task so I remember what to do
- As a user, I can see all my tasks so I know what's pending
- As a user, I can mark tasks complete so I track progress
- As a user, I can delete tasks I no longer need

### Success Metrics
- Task operations complete in <100ms
- Zero data loss on normal exit

### Out of Scope
- Due dates, priorities, categories
- Multi-user support
- Cloud sync

## Technical Documentation

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLI       │────▶│   Core      │────▶│   Storage   │
│   Parser    │     │   Logic     │     │   (JSON)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Tech Stack
- **Language:** Python 3.8+
- **Storage:** JSON file (`~/.todo.json`)
- **Dependencies:** None (stdlib only)

### Data Model

```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "completed": false,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "next_id": 2
}
```

### CLI Interface

```bash
todo add "Task description"    # Add new task
todo list                      # Show all tasks
todo done <id>                 # Mark task complete
todo delete <id>               # Remove task
```

### Module Structure

```
todo/
├── __main__.py    # Entry point, CLI parsing
├── core.py        # Business logic (add, list, complete, delete)
└── storage.py     # JSON file read/write
```

### Key Functions

| Function | Input | Output |
|----------|-------|--------|
| `add_task(desc)` | string | task object |
| `list_tasks()` | - | list of tasks |
| `complete_task(id)` | int | bool (success) |
| `delete_task(id)` | int | bool (success) |

### Error Handling
- Invalid task ID → "Task not found" message
- Corrupted JSON → Reset to empty state with warning
- File permissions → Clear error message

### Testing
- Unit tests for core logic
- Integration tests for CLI commands
- Edge cases: empty list, invalid IDs, special characters

## Implementation Status
- [x] Setup complete
- [ ] Implementation in progress
- [ ] Code review passed
- [ ] Security review passed