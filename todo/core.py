"""Core business logic for ToDo application."""
from datetime import datetime
from typing import Dict, List, Optional, Any
from todo.storage import Storage


class TodoApp:
    """Main application class handling task operations."""
    
    def __init__(self, storage: Storage = None):
        """Initialize ToDo app with storage.
        
        Args:
            storage: Storage instance. Creates default if None.
        """
        self.storage = storage if storage else Storage()
    
    def add_task(self, description: str) -> Dict[str, Any]:
        """Add a new task.
        
        Args:
            description: Task description.
            
        Returns:
            Dictionary representing the created task.
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        data = self.storage.load()
        
        task = {
            "id": data["next_id"],
            "description": description.strip(),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        data["tasks"].append(task)
        data["next_id"] += 1
        
        self.storage.save(data)
        return task
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks.
        
        Returns:
            List of task dictionaries.
        """
        data = self.storage.load()
        return data["tasks"]
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed.
        
        Args:
            task_id: ID of the task to complete.
            
        Returns:
            True if task was found and completed, False otherwise.
        """
        data = self.storage.load()
        
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                self.storage.save(data)
                return True
        
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete.
            
        Returns:
            True if task was found and deleted, False otherwise.
        """
        data = self.storage.load()
        
        original_length = len(data["tasks"])
        data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
        
        if len(data["tasks"]) < original_length:
            self.storage.save(data)
            return True
        
        return False
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve.
            
        Returns:
            Task dictionary if found, None otherwise.
        """
        data = self.storage.load()
        
        for task in data["tasks"]:
            if task["id"] == task_id:
                return task
        
        return None
