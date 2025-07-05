import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any
from config.settings import get_config

class Memory:
    """Memory system for storing and retrieving agent interactions"""
    
    def __init__(self, path: str = None):
        config = get_config()
        self.path = path or config.get("memory_path", "data/memory.json")
        self.data = self._load()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
    
    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load memory data from file"""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Error loading memory from {self.path}: {e}")
                return {}
        return {}
    
    def _save(self):
        """Save memory data to file"""
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving memory to {self.path}: {e}")
    
    def store(self, goal: str, step: Dict[str, Any], result: str):
        """Store a step and its result for a given goal"""
        timestamp = datetime.now().isoformat()
        
        entry = {
            "step": step,
            "result": result,
            "timestamp": timestamp
        }
        
        if goal not in self.data:
            self.data[goal] = []
        
        self.data[goal].append(entry)
        self._save()
        
        logging.info(f"Stored memory entry for goal: {goal}")
    
    def retrieve(self, goal: str) -> List[Dict[str, Any]]:
        """Retrieve all stored entries for a given goal"""
        return self.data.get(goal, [])
    
    def get_recent_context(self, goal: str, max_entries: int = 5) -> str:
        """Get recent context for a goal as formatted string"""
        entries = self.retrieve(goal)
        if not entries:
            return "No prior context available."
        
        # Get the most recent entries
        recent_entries = entries[-max_entries:]
        
        context_parts = []
        for entry in recent_entries:
            step_desc = entry["step"].get("action", "unknown")
            result_preview = entry["result"][:200] + "..." if len(entry["result"]) > 200 else entry["result"]
            context_parts.append(f"- {step_desc}: {result_preview}")
        
        return "\n".join(context_parts)
    
    def clear_goal(self, goal: str):
        """Clear all memory entries for a specific goal"""
        if goal in self.data:
            del self.data[goal]
            self._save()
            logging.info(f"Cleared memory for goal: {goal}")
    
    def get_all_goals(self) -> List[str]:
        """Get list of all goals with stored memory"""
        return list(self.data.keys())
    
    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics"""
        total_entries = sum(len(entries) for entries in self.data.values())
        return {
            "total_goals": len(self.data),
            "total_entries": total_entries
        }
