import json
import logging
from typing import List, Dict, Any
from core.llm_interface import call_model
from skills import list_available_skills

def plan_steps(goal: str, prior_context: str) -> List[Dict[str, Any]]:
    """Generate a plan of steps to achieve the given goal"""
    
    available_skills = list_available_skills()
    skills_description = _format_skills_description(available_skills)
    
    prompt = f"""You are Optimus Bot, a coding agent that helps improve and analyze code.

Goal: {goal}

Prior Context from Memory:
{prior_context}

Available Skills:
{skills_description}

Your task is to create a step-by-step plan to achieve the goal. Return your response as a JSON array of steps.

Each step should have this format:
{{"action": "skill_name", "params": {{"param1": "value1", "param2": "value2"}}}}

Example response:
[
    {{"action": "generate_task_code", "params": {{"task": "improve error handling in patch_engine.py"}}}},
    {{"action": "trace_variable_flow", "params": {{"file": "patch_engine.py", "variable": "patch_result"}}}}
]

Important:
- Only use skills from the available skills list
- Be specific with parameters
- Focus on actionable steps
- Return valid JSON only

Plan:"""

    try:
        response = call_model(prompt, max_tokens=1024, temperature=0.3)
        logging.debug(f"Planner raw response: {response}")
        
        # Try to parse the JSON response
        steps = _parse_plan_response(response)
        
        # Validate the steps
        validated_steps = _validate_steps(steps, available_skills)
        
        logging.info(f"Generated plan with {len(validated_steps)} steps")
        return validated_steps
        
    except Exception as e:
        logging.error(f"Error generating plan: {e}")
        # Return a fallback plan
        return _get_fallback_plan(goal)

def _format_skills_description(skills: List[str]) -> str:
    """Format the available skills for the prompt"""
    skill_descriptions = {
        "generate_task_code": "Generate code for a specific task or improvement",
        "trace_variable_flow": "Trace how variables flow through code",
        "scan_codebase": "Scan and analyze the codebase structure",
        "analyze_dependencies": "Analyze code dependencies and imports"
    }
    
    formatted = []
    for skill in skills:
        desc = skill_descriptions.get(skill, "No description available")
        formatted.append(f"- {skill}: {desc}")
    
    return "\n".join(formatted)

def _parse_plan_response(response: str) -> List[Dict[str, Any]]:
    """Parse the LLM response to extract the plan steps"""
    # Try to find JSON in the response
    response = response.strip()
    
    # Look for JSON array markers
    start_idx = response.find('[')
    end_idx = response.rfind(']')
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError("No JSON array found in response")
    
    json_str = response[start_idx:end_idx + 1]
    
    try:
        steps = json.loads(json_str)
        if not isinstance(steps, list):
            raise ValueError("Response is not a list")
        return steps
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        raise ValueError(f"Invalid JSON in response: {e}")

def _validate_steps(steps: List[Dict[str, Any]], available_skills: List[str]) -> List[Dict[str, Any]]:
    """Validate and filter the generated steps"""
    validated = []
    
    for step in steps:
        if not isinstance(step, dict):
            logging.warning(f"Skipping invalid step (not a dict): {step}")
            continue
        
        action = step.get("action")
        if not action:
            logging.warning(f"Skipping step without action: {step}")
            continue
        
        if action not in available_skills:
            logging.warning(f"Skipping step with unknown skill: {action}")
            continue
        
        # Ensure params is a dict
        if "params" not in step:
            step["params"] = {}
        elif not isinstance(step["params"], dict):
            step["params"] = {}
        
        validated.append(step)
    
    return validated

def _get_fallback_plan(goal: str) -> List[Dict[str, Any]]:
    """Generate a fallback plan when the LLM fails"""
    logging.info("Using fallback plan")
    
    # Simple fallback based on common patterns
    if "patch" in goal.lower() or "improve" in goal.lower():
        return [
            {"action": "generate_task_code", "params": {"task": goal}},
            {"action": "trace_variable_flow", "params": {"file": "patch_engine.py"}}
        ]
    else:
        return [
            {"action": "generate_task_code", "params": {"task": goal}}
        ]
