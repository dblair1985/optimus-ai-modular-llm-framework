"""
Code Scanner Utility

This module provides functionality to scan and analyze codebases,
extracting relevant information for the LLM context.
"""

import os
import logging
from typing import List, Dict, Optional
from pathlib import Path

def scan_codebase(root: str = ".", extensions: List[str] = None, max_files: int = 10, 
                 max_chars_per_file: int = 1000) -> str:
    """
    Scan the codebase and return a summary of relevant files
    
    Args:
        root: Root directory to scan
        extensions: File extensions to include (default: [".py"])
        max_files: Maximum number of files to include
        max_chars_per_file: Maximum characters to read from each file
    
    Returns:
        str: Formatted string containing code snippets and structure
    """
    if extensions is None:
        extensions = [".py"]
    
    logging.info(f"Scanning codebase from {root} for extensions: {extensions}")
    
    try:
        chunks = []
        file_count = 0
        
        for dirpath, dirnames, filenames in os.walk(root):
            # Skip common directories that shouldn't be scanned
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and 
                          d not in ['__pycache__', 'node_modules', 'venv', 'env']]
            
            for filename in filenames:
                if file_count >= max_files:
                    break
                
                if any(filename.endswith(ext) for ext in extensions):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()[:max_chars_per_file]
                            
                        # Add file header and content
                        chunk = f"\n--- {relative_path} ---\n{content}"
                        if len(content) == max_chars_per_file:
                            chunk += "\n... (truncated)"
                        
                        chunks.append(chunk)
                        file_count += 1
                        
                    except Exception as e:
                        logging.warning(f"Could not read file {file_path}: {e}")
                        continue
            
            if file_count >= max_files:
                break
        
        result = "\n".join(chunks)
        logging.info(f"Scanned {file_count} files, {len(result)} total characters")
        
        return result if result else "No relevant files found in codebase."
        
    except Exception as e:
        logging.error(f"Error scanning codebase: {e}")
        return f"Error scanning codebase: {str(e)}"

def get_file_structure(root: str = ".", max_depth: int = 3) -> str:
    """
    Get a tree-like representation of the file structure
    
    Args:
        root: Root directory to scan
        max_depth: Maximum depth to traverse
    
    Returns:
        str: Tree representation of the file structure
    """
    logging.info(f"Getting file structure from {root}")
    
    try:
        lines = []
        
        def add_items(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                
                for i, item in enumerate(items):
                    # Skip hidden files and common ignore patterns
                    if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules']:
                        continue
                    
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    lines.append(f"{prefix}{current_prefix}{item.name}")
                    
                    if item.is_dir() and depth < max_depth:
                        extension = "    " if is_last else "│   "
                        add_items(item, prefix + extension, depth + 1)
                        
            except PermissionError:
                lines.append(f"{prefix}└── [Permission Denied]")
        
        root_path = Path(root)
        lines.append(f"{root_path.name}/")
        add_items(root_path)
        
        return "\n".join(lines)
        
    except Exception as e:
        logging.error(f"Error getting file structure: {e}")
        return f"Error getting file structure: {str(e)}"

def analyze_imports(file_path: str) -> Dict[str, List[str]]:
    """
    Analyze imports in a Python file
    
    Args:
        file_path: Path to the Python file
    
    Returns:
        dict: Dictionary with 'standard', 'third_party', and 'local' import lists
    """
    import ast
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        imports = {
            'standard': [],
            'third_party': [],
            'local': []
        }
        
        # Standard library modules (partial list)
        standard_libs = {
            'os', 'sys', 'json', 'logging', 'datetime', 'pathlib', 'typing',
            'collections', 'itertools', 'functools', 're', 'math', 'random',
            'urllib', 'http', 'ast', 'importlib'
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    _categorize_import(module_name, imports, standard_libs)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module.split('.')[0]
                    _categorize_import(module_name, imports, standard_libs)
        
        return imports
        
    except Exception as e:
        logging.error(f"Error analyzing imports in {file_path}: {e}")
        return {'standard': [], 'third_party': [], 'local': []}

def _categorize_import(module_name: str, imports: Dict[str, List[str]], 
                      standard_libs: set):
    """Categorize an import as standard, third-party, or local"""
    if module_name in standard_libs:
        if module_name not in imports['standard']:
            imports['standard'].append(module_name)
    elif module_name.startswith('.') or '.' not in module_name:
        if module_name not in imports['local']:
            imports['local'].append(module_name)
    else:
        if module_name not in imports['third_party']:
            imports['third_party'].append(module_name)

def find_functions(file_path: str) -> List[Dict[str, any]]:
    """
    Find all function definitions in a Python file
    
    Args:
        file_path: Path to the Python file
    
    Returns:
        list: List of dictionaries containing function information
    """
    import ast
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'docstring': ast.get_docstring(node),
                    'is_async': isinstance(node, ast.AsyncFunctionDef)
                }
                functions.append(func_info)
        
        return functions
        
    except Exception as e:
        logging.error(f"Error finding functions in {file_path}: {e}")
        return []

def get_code_metrics(file_path: str) -> Dict[str, int]:
    """
    Get basic code metrics for a Python file
    
    Args:
        file_path: Path to the Python file
    
    Returns:
        dict: Dictionary containing various code metrics
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'comment_ratio': comment_lines / max(code_lines, 1)
        }
        
    except Exception as e:
        logging.error(f"Error getting code metrics for {file_path}: {e}")
        return {}
