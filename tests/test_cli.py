"""Integration tests for CLI commands."""
import unittest
import tempfile
import os
import sys
from io import StringIO
from unittest.mock import patch
from todo.__main__ import main
from todo.storage import Storage


class TestCLI(unittest.TestCase):
    """Test cases for CLI interface."""
    
    def setUp(self):
        """Create a temporary storage file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Patch the Storage class to use our temp file
        self.storage_patcher = patch('todo.__main__.TodoApp')
        self.mock_app_class = self.storage_patcher.start()
        
        # Create a real TodoApp with temp storage
        from todo.core import TodoApp
        self.real_app = TodoApp(Storage(self.temp_file.name))
        self.mock_app_class.return_value = self.real_app
    
    def tearDown(self):
        """Clean up temporary file and patches."""
        self.storage_patcher.stop()
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def run_cli(self, args):
        """Helper to run CLI with arguments and capture output."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        old_argv = sys.argv
        sys.argv = ['todo'] + args
        
        try:
            main()
            output = sys.stdout.getvalue()
            return output, 0
        except SystemExit as e:
            output = sys.stdout.getvalue()
            return output, e.code
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv
    
    def test_add_command(self):
        """Test add command."""
        output, code = self.run_cli(['add', 'Test task'])
        self.assertEqual(code, 0)
        self.assertIn('Added task 1', output)
        self.assertIn('Test task', output)
    
    def test_add_command_multiword(self):
        """Test add command with multi-word description."""
        output, code = self.run_cli(['add', 'Buy', 'groceries', 'today'])
        self.assertEqual(code, 0)
        self.assertIn('Buy groceries today', output)
    
    def test_add_command_missing_description(self):
        """Test add command without description."""
        output, code = self.run_cli(['add'])
        self.assertEqual(code, 1)
        self.assertIn('Error', output)
    
    def test_list_command_empty(self):
        """Test list command with no tasks."""
        output, code = self.run_cli(['list'])
        self.assertEqual(code, 0)
        self.assertIn('No tasks found', output)
    
    def test_list_command_with_tasks(self):
        """Test list command with tasks."""
        self.run_cli(['add', 'Task 1'])
        self.run_cli(['add', 'Task 2'])
        
        output, code = self.run_cli(['list'])
        self.assertEqual(code, 0)
        self.assertIn('Task 1', output)
        self.assertIn('Task 2', output)
        self.assertIn('1.', output)
        self.assertIn('2.', output)
    
    def test_done_command(self):
        """Test done command."""
        self.run_cli(['add', 'Task to complete'])
        
        output, code = self.run_cli(['done', '1'])
        self.assertEqual(code, 0)
        self.assertIn('marked as complete', output)
        
        # Verify task is marked complete
        list_output, _ = self.run_cli(['list'])
        self.assertIn('✓', list_output)
    
    def test_done_command_invalid_id(self):
        """Test done command with invalid task ID."""
        output, code = self.run_cli(['done', '999'])
        self.assertEqual(code, 1)
        self.assertIn('not found', output)
    
    def test_done_command_missing_id(self):
        """Test done command without task ID."""
        output, code = self.run_cli(['done'])
        self.assertEqual(code, 1)
        self.assertIn('Error', output)
    
    def test_done_command_non_numeric_id(self):
        """Test done command with non-numeric ID."""
        output, code = self.run_cli(['done', 'abc'])
        self.assertEqual(code, 1)
        self.assertIn('must be a number', output)
    
    def test_delete_command(self):
        """Test delete command."""
        self.run_cli(['add', 'Task to delete'])
        
        output, code = self.run_cli(['delete', '1'])
        self.assertEqual(code, 0)
        self.assertIn('deleted', output)
        
        # Verify task is deleted
        list_output, _ = self.run_cli(['list'])
        self.assertIn('No tasks found', list_output)
    
    def test_delete_command_invalid_id(self):
        """Test delete command with invalid task ID."""
        output, code = self.run_cli(['delete', '999'])
        self.assertEqual(code, 1)
        self.assertIn('not found', output)
    
    def test_unknown_command(self):
        """Test unknown command."""
        output, code = self.run_cli(['unknown'])
        self.assertEqual(code, 1)
        self.assertIn('Unknown command', output)
    
    def test_no_command(self):
        """Test running without a command."""
        output, code = self.run_cli([])
        self.assertEqual(code, 1)
        self.assertIn('Usage', output)


if __name__ == '__main__':
    unittest.main()
