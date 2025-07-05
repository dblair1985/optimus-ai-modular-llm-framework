import logging
from typing import Optional
from core.planner import plan_steps
from core.memory import Memory
from skills import registry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global memory instance
memory = Memory()

def run_agent(goal: str, max_iterations: int = 10) -> bool:
    """
    Run the agent loop to achieve the given goal
    
    Args:
        goal: The goal to achieve
        max_iterations: Maximum number of iterations to prevent infinite loops
    
    Returns:
        bool: True if successful, False if failed
    """
    logging.info(f"🚀 Starting Optimus Agent with goal: {goal}")
    
    try:
        # Retrieve prior context from memory
        prior_context = memory.get_recent_context(goal)
        logging.info(f"Retrieved prior context: {len(prior_context)} characters")
        
        # Generate plan
        logging.info("📋 Generating execution plan...")
        plan = plan_steps(goal, prior_context)
        
        if not plan:
            logging.error("❌ Failed to generate a valid plan")
            return False
        
        logging.info(f"📝 Generated plan with {len(plan)} steps:")
        for i, step in enumerate(plan, 1):
            logging.info(f"  {i}. {step['action']} - {step.get('params', {})}")
        
        # Execute plan steps
        success_count = 0
        for i, step in enumerate(plan, 1):
            if i > max_iterations:
                logging.warning(f"⚠️ Reached maximum iterations ({max_iterations}), stopping")
                break
            
            logging.info(f"🔄 Executing step {i}/{len(plan)}: {step['action']}")
            
            success = _execute_step(goal, step)
            if success:
                success_count += 1
            else:
                logging.warning(f"⚠️ Step {i} failed, continuing with next step")
        
        # Report results
        success_rate = success_count / len(plan) if plan else 0
        logging.info(f"✅ Agent execution completed: {success_count}/{len(plan)} steps successful ({success_rate:.1%})")
        
        return success_rate > 0.5  # Consider successful if more than 50% of steps succeeded
        
    except Exception as e:
        logging.error(f"❌ Agent loop failed: {e}", exc_info=True)
        return False

def _execute_step(goal: str, step: dict) -> bool:
    """
    Execute a single step of the plan
    
    Args:
        goal: The overall goal
        step: The step to execute
    
    Returns:
        bool: True if successful, False if failed
    """
    action = step.get("action")
    params = step.get("params", {})
    
    try:
        # Resolve the skill function
        skill_func = registry.resolve(action)
        if skill_func is None:
            logging.error(f"❌ Skill '{action}' not found in registry")
            return False
        
        logging.debug(f"🔧 Calling {action} with params: {params}")
        
        # Execute the skill
        result = skill_func(**params)
        
        # Store the result in memory
        memory.store(goal, step, str(result))
        
        # Log the result (truncated for readability)
        result_preview = str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
        logging.info(f"✅ Step completed. Result: {result_preview}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Error executing step {action}: {e}", exc_info=True)
        
        # Store the error in memory for learning
        error_msg = f"Error: {str(e)}"
        memory.store(goal, step, error_msg)
        
        return False

def get_agent_status() -> dict:
    """Get the current status of the agent"""
    stats = memory.get_stats()
    return {
        "memory_stats": stats,
        "available_skills": len(registry.registry),
        "recent_goals": memory.get_all_goals()[-5:]  # Last 5 goals
    }

def clear_agent_memory(goal: Optional[str] = None):
    """Clear agent memory for a specific goal or all goals"""
    if goal:
        memory.clear_goal(goal)
        logging.info(f"🧹 Cleared memory for goal: {goal}")
    else:
        # This would require implementing a clear_all method in Memory class
        logging.info("🧹 Memory clearing not implemented for all goals")
