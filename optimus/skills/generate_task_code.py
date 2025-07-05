"""
Generate Task Code Skill

This skill generates code for specific tasks using the LLM.
It can create new functions, patches, or improvements to existing code.
"""

import logging
from typing import Optional
from core.llm_interface import call_model
from utils.code_scanner import scan_codebase

def generate_task_code(task: str, context_file: Optional[str] = None, max_tokens: int = 1024, **kwargs) -> str:
    """
    Generate code for a specific task
    
    Args:
        task: Description of the task to generate code for
        context_file: Optional file to provide additional context
        max_tokens: Maximum tokens for the LLM response
        **kwargs: Additional parameters (for flexibility)
    
    Returns:
        str: Generated code or patch
    """
    logging.info(f"Generating code for task: {task}")
    
    try:
        # Get codebase context
        code_context = scan_codebase()
        
        # Add specific file context if provided
        file_context = ""
        if context_file:
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    file_context = f"\n\nSpecific file context from {context_file}:\n```\n{file_content}\n```"
            except Exception as e:
                logging.warning(f"Could not read context file {context_file}: {e}")
        
        # Construct the prompt
        prompt = f"""You are an expert Python developer. Generate code for the following task:

Task: {task}

Codebase Context:
{code_context}
{file_context}

Instructions:
1. Write clean, well-documented Python code
2. Follow best practices and PEP 8 style guidelines
3. Include error handling where appropriate
4. If this is a patch/improvement, show only the changes needed
5. If this is a new function, provide the complete implementation
6. Add docstrings and comments for clarity

Return ONLY the code or patch diff, no additional explanation:"""

        # Generate the code
        response = call_model(prompt, max_tokens=max_tokens, temperature=0.3)
        
        # Clean up the response
        code = _clean_code_response(response)
        
        logging.info(f"Generated {len(code)} characters of code")
        logging.debug(f"Generated code preview: {code[:200]}...")
        
        return code
        
    except Exception as e:
        logging.error(f"Error generating task code: {e}")
        return f"# Error generating code for task: {task}\n# Error: {str(e)}"

def _clean_code_response(response: str) -> str:
    """Clean up the LLM response to extract just the code"""
    # Remove common markdown code block markers
    response = response.strip()
    
    # Remove ```python or ``` markers
    if response.startswith('```python'):
        response = response[9:]
    elif response.startswith('```'):
        response = response[3:]
    
    if response.endswith('```'):
        response = response[:-3]
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    # If the response is empty or too short, provide a placeholder
    if len(response) < 10:
        return "# Generated code placeholder\npass"
    
    return response

def generate_patch(file_path: str, improvement_description: str) -> str:
    """
    Generate a patch for an existing file
    
    Args:
        file_path: Path to the file to patch
        improvement_description: Description of the improvement to make
    
    Returns:
        str: Patch in diff format
    """
    logging.info(f"Generating patch for {file_path}: {improvement_description}")
    
    try:
        # Read the existing file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Generate improved version
        task = f"Improve the file {file_path} by {improvement_description}"
        improved_code = generate_task_code(task, context_file=file_path)
        
        # Create a simple diff representation
        patch = f"""--- {file_path} (original)
+++ {file_path} (improved)
@@ Improvement: {improvement_description} @@

Original code:
{original_content[:500]}...

Improved code:
{improved_code}
"""
        
        return patch
        
    except Exception as e:
        logging.error(f"Error generating patch: {e}")
        return f"# Error generating patch for {file_path}\n# Error: {str(e)}"

def generate_function(function_name: str, description: str, parameters: Optional[str] = None) -> str:
    """
    Generate a complete function implementation
    
    Args:
        function_name: Name of the function to generate
        description: Description of what the function should do
        parameters: Optional parameter specification
    
    Returns:
        str: Complete function implementation
    """
    params_info = f" with parameters: {parameters}" if parameters else ""
    task = f"Create a function named '{function_name}' that {description}{params_info}"
    
    return generate_task_code(task)
