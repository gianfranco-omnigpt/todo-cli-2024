"""Storage module for handling JSON file operations."""
import json
import os
from pathlib import Path
from typing import Dict, List, Any


class Storage:
    """Handles reading and writing task data to JSON file."""
    
    def __init__(self, filepath: str = None):
        """Initialize storage with file path.
        
        Args:
            filepath: Path to JSON file. Defaults to ~/.todo.json
        """
        if filepath is None:
            filepath = os.path.join(str(Path.home()), '.todo.json')
        self.filepath = filepath
    
    def load(self) -> Dict[str, Any]:
        """Load data from JSON file.
        
        Returns:
            Dictionary containing tasks and next_id.
            Returns empty structure if file doesn't exist or is corrupted.
        """
        if not os.path.exists(self.filepath):
            return {"tasks": [], "next_id": 1}
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate data structure
                if not isinstance(data, dict) or 'tasks' not in data or 'next_id' not in data:
                    print(f"Warning: Corrupted data in {self.filepath}. Resetting to empty state.")
                    return {"tasks": [], "next_id": 1}
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error reading {self.filepath}: {e}. Resetting to empty state.")
            return {"tasks": [], "next_id": 1}
    
    def save(self, data: Dict[str, Any]) -> bool:
        """Save data to JSON file.
        
        Args:
            data: Dictionary containing tasks and next_id.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.filepath) or '.', exist_ok=True)
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Failed to write to {self.filepath}: {e}")
            return False
