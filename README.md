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

## Installation

```bash
# Clone the repository
git clone https://github.com/gianfranco-omnigpt/todo-cli-2024.git
cd todo-cli-2024

# Install the package
pip install -e .
```

## Usage

After installation, use the `todo` command:

```bash
# Add a task
todo add "Buy groceries"
todo add "Write documentation"

# List all tasks
todo list

# Mark a task as complete
todo done 1

# Delete a task
todo delete 2
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m unittest tests.test_core
python -m unittest tests.test_storage
python -m unittest tests.test_cli
```

## Project Structure

```
todo-cli-2024/
├── todo/
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # CLI entry point
│   ├── core.py           # Business logic
│   └── storage.py        # JSON storage handler
├── tests/
│   ├── __init__.py
│   ├── test_core.py      # Core logic tests
│   ├── test_storage.py   # Storage tests
│   └── test_cli.py       # CLI integration tests
├── .gitignore
├── setup.py
├── requirements.txt
└── README.md
```

## Implementation Status
- [x] Setup complete
- [x] Implementation complete
- [ ] Code review passed
- [ ] Security review passed

## Development

### Key Implementation Details

1. **Storage Layer** (`storage.py`):
   - JSON-based persistence to `~/.todo.json`
   - Graceful handling of corrupted data
   - Automatic directory creation

2. **Core Logic** (`core.py`):
   - TodoApp class manages all business logic
   - Task operations: add, list, complete, delete
   - Auto-incrementing task IDs
   - ISO 8601 timestamps

3. **CLI Interface** (`__main__.py`):
   - Simple command parsing
   - Clear error messages
   - Exit codes for error conditions

4. **Testing**:
   - 30+ test cases covering unit and integration scenarios
   - Temporary file fixtures for isolated tests
   - Edge case coverage (empty descriptions, invalid IDs, special characters)

### Code Quality Features

- ✅ Clean, modular architecture
- ✅ Comprehensive docstrings
- ✅ Type hints for better IDE support
- ✅ Error handling with user-friendly messages
- ✅ No external dependencies (stdlib only)
- ✅ Full test coverage
- ✅ PEP 8 compliant code style