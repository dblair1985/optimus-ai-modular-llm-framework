"""
Skills module for Optimus Bot

This module provides a registry system for hot-loadable skills.
Skills are functions that the agent can execute to accomplish tasks.
"""

import logging
import importlib
import os
from typing import Dict, Callable, List, Any

class SkillRegistry:
    """Registry for managing and executing skills"""
    
    def __init__(self):
        self.registry: Dict[str, Callable] = {}
        self._load_skills()
    
    def _load_skills(self):
        """Load all available skills"""
        try:
            # Import core skills
            from skills.generate_task_code import generate_task_code
            from skills.trace_variable_flow import trace_variable_flow
            
            # Register core skills
            self.register("generate_task_code", generate_task_code)
            self.register("trace_variable_flow", trace_variable_flow)
            
            logging.info(f"Loaded {len(self.registry)} skills")
            
        except ImportError as e:
            logging.warning(f"Some skills could not be imported: {e}")
    
    def register(self, name: str, func: Callable):
        """Register a skill function"""
        self.registry[name] = func
        logging.debug(f"Registered skill: {name}")
    
    def resolve(self, name: str) -> Callable:
        """Resolve a skill by name"""
        if name not in self.registry:
            raise ValueError(f"Skill '{name}' not found in registry")
        return self.registry[name]
    
    def list_skills(self) -> List[str]:
        """List all available skills"""
        return list(self.registry.keys())
    
    def reload_skills(self):
        """Reload all skills (hot-loading)"""
        logging.info("Reloading skills...")
        self.registry.clear()
        self._load_skills()
    
    def get_skill_info(self, name: str) -> Dict[str, Any]:
        """Get information about a skill"""
        if name not in self.registry:
            return {"error": f"Skill '{name}' not found"}
        
        func = self.registry[name]
        return {
            "name": name,
            "doc": func.__doc__ or "No documentation available",
            "module": func.__module__,
            "available": True
        }

# Global registry instance
registry = SkillRegistry()

# Convenience functions for backward compatibility
def resolve(name: str) -> Callable:
    """Resolve a skill by name"""
    return registry.resolve(name)

def list_available_skills() -> List[str]:
    """List all available skills"""
    return registry.list_skills()

def reload_skills():
    """Reload all skills"""
    registry.reload_skills()

def get_skill_info(name: str) -> Dict[str, Any]:
    """Get information about a skill"""
    return registry.get_skill_info(name)
