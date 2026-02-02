"""CLI entry point for ToDo application."""
import sys
from todo.core import TodoApp


def format_task(task):
    """Format a task for display.
    
    Args:
        task: Task dictionary.
        
    Returns:
        Formatted string representation of the task.
    """
    status = "✓" if task["completed"] else " "
    return f"[{status}] {task['id']}. {task['description']}"


def main():
    """Main CLI entry point."""
    app = TodoApp()
    
    if len(sys.argv) < 2:
        print("Usage: python -m todo <command> [arguments]")
        print("")
        print("Commands:")
        print("  add <description>    Add a new task")
        print("  list                 List all tasks")
        print("  done <id>            Mark task as complete")
        print("  delete <id>          Delete a task")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Task description required")
                sys.exit(1)
            
            description = " ".join(sys.argv[2:])
            task = app.add_task(description)
            print(f"Added task {task['id']}: {task['description']}")
        
        elif command == "list":
            tasks = app.list_tasks()
            
            if not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    print(format_task(task))
        
        elif command == "done":
            if len(sys.argv) < 3:
                print("Error: Task ID required")
                sys.exit(1)
            
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print("Error: Task ID must be a number")
                sys.exit(1)
            
            if app.complete_task(task_id):
                print(f"Task {task_id} marked as complete")
            else:
                print(f"Error: Task {task_id} not found")
                sys.exit(1)
        
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Task ID required")
                sys.exit(1)
            
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print("Error: Task ID must be a number")
                sys.exit(1)
            
            if app.delete_task(task_id):
                print(f"Task {task_id} deleted")
            else:
                print(f"Error: Task {task_id} not found")
                sys.exit(1)
        
        else:
            print(f"Error: Unknown command '{command}'")
            sys.exit(1)
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
