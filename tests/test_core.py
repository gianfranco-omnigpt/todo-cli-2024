"""Unit tests for core module."""
import unittest
import tempfile
import os
from todo.core import TodoApp
from todo.storage import Storage


class TestTodoApp(unittest.TestCase):
    """Test cases for TodoApp class."""
    
    def setUp(self):
        """Create a temporary storage for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        storage = Storage(self.temp_file.name)
        self.app = TodoApp(storage)
    
    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.app.add_task("Buy groceries")
        
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Buy groceries")
        self.assertFalse(task["completed"])
        self.assertIn("created_at", task)
    
    def test_add_task_with_whitespace(self):
        """Test adding a task with leading/trailing whitespace."""
        task = self.app.add_task("  Task with spaces  ")
        self.assertEqual(task["description"], "Task with spaces")
    
    def test_add_task_empty_description(self):
        """Test adding a task with empty description raises error."""
        with self.assertRaises(ValueError):
            self.app.add_task("")
        
        with self.assertRaises(ValueError):
            self.app.add_task("   ")
    
    def test_list_tasks_empty(self):
        """Test listing tasks when none exist."""
        tasks = self.app.list_tasks()
        self.assertEqual(tasks, [])
    
    def test_list_tasks(self):
        """Test listing multiple tasks."""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        
        tasks = self.app.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["description"], "Task 1")
        self.assertEqual(tasks[1]["description"], "Task 2")
    
    def test_complete_task(self):
        """Test completing a task."""
        task = self.app.add_task("Task to complete")
        task_id = task["id"]
        
        result = self.app.complete_task(task_id)
        self.assertTrue(result)
        
        updated_task = self.app.get_task(task_id)
        self.assertTrue(updated_task["completed"])
    
    def test_complete_nonexistent_task(self):
        """Test completing a task that doesn't exist."""
        result = self.app.complete_task(999)
        self.assertFalse(result)
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = self.app.add_task("Task to delete")
        task_id = task["id"]
        
        result = self.app.delete_task(task_id)
        self.assertTrue(result)
        
        tasks = self.app.list_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        result = self.app.delete_task(999)
        self.assertFalse(result)
    
    def test_get_task(self):
        """Test getting a specific task."""
        task = self.app.add_task("Test task")
        task_id = task["id"]
        
        retrieved_task = self.app.get_task(task_id)
        self.assertEqual(retrieved_task["id"], task_id)
        self.assertEqual(retrieved_task["description"], "Test task")
    
    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        task = self.app.get_task(999)
        self.assertIsNone(task)
    
    def test_task_id_increments(self):
        """Test that task IDs increment correctly."""
        task1 = self.app.add_task("Task 1")
        task2 = self.app.add_task("Task 2")
        task3 = self.app.add_task("Task 3")
        
        self.assertEqual(task1["id"], 1)
        self.assertEqual(task2["id"], 2)
        self.assertEqual(task3["id"], 3)
    
    def test_special_characters_in_description(self):
        """Test adding tasks with special characters."""
        special_chars = "Task with 'quotes', \"double quotes\", and symbols: @#$%"
        task = self.app.add_task(special_chars)
        self.assertEqual(task["description"], special_chars)
        
        retrieved = self.app.get_task(task["id"])
        self.assertEqual(retrieved["description"], special_chars)


if __name__ == '__main__':
    unittest.main()
