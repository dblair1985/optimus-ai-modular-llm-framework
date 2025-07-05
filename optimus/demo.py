#!/usr/bin/env python3
"""
Demo script for Optimus Bot

This script demonstrates the key features of the Optimus Bot system
without requiring external dependencies.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.agent_loop import run_agent, get_agent_status
from skills import list_available_skills, get_skill_info
from core.memory import Memory
from utils.code_scanner import scan_codebase, get_file_structure

def demo_skills():
    """Demonstrate the skills system"""
    print("🔧 Available Skills:")
    print("=" * 50)
    
    skills = list_available_skills()
    for skill in skills:
        info = get_skill_info(skill)
        print(f"• {skill}")
        print(f"  Description: {info.get('doc', 'No description')}")
        print()

def demo_code_scanning():
    """Demonstrate code scanning capabilities"""
    print("📁 File Structure:")
    print("=" * 50)
    structure = get_file_structure(".", max_depth=2)
    print(structure)
    print()
    
    print("🔍 Code Scanning:")
    print("=" * 50)
    code_summary = scan_codebase(".", max_files=3, max_chars_per_file=200)
    print(code_summary)
    print()

def demo_memory():
    """Demonstrate memory system"""
    print("🧠 Memory System:")
    print("=" * 50)
    
    memory = Memory()
    stats = memory.get_stats()
    print(f"Total goals in memory: {stats['total_goals']}")
    print(f"Total entries: {stats['total_entries']}")
    
    # Add a test entry
    test_goal = "Demo goal"
    test_step = {"action": "demo_action", "params": {"test": "value"}}
    test_result = "Demo result for testing memory"
    
    memory.store(test_goal, test_step, test_result)
    
    # Retrieve and display
    context = memory.get_recent_context(test_goal)
    print(f"\nRecent context for '{test_goal}':")
    print(context)
    print()

def demo_agent():
    """Demonstrate agent execution"""
    print("🤖 Agent Execution:")
    print("=" * 50)
    
    # Test with a simple goal
    goal = "Analyze the test_example.py file"
    print(f"Goal: {goal}")
    print()
    
    success = run_agent(goal, max_iterations=3)
    print(f"\nAgent execution {'succeeded' if success else 'failed'}")
    
    # Show agent status
    status = get_agent_status()
    print(f"Agent Status: {status}")
    print()

def main():
    """Run the complete demo"""
    print("🚀 Optimus Bot Demo")
    print("=" * 50)
    print("This demo showcases the Optimus Bot capabilities")
    print("without requiring external LLM dependencies.")
    print()
    
    try:
        demo_skills()
        demo_code_scanning()
        demo_memory()
        demo_agent()
        
        print("✅ Demo completed successfully!")
        print("\nTo use with a real Mistral model:")
        print("1. Install ctransformers: pip install ctransformers")
        print("2. Download a Mistral GGUF model")
        print("3. Set MODEL_PATH in config/settings.py")
        print("4. Run: python main.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
