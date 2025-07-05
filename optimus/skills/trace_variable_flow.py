"""
Trace Variable Flow Skill

This skill analyzes how variables flow through code, tracking their usage,
modifications, and dependencies across functions and modules.
"""

import ast
import logging
from typing import Dict, List, Set, Optional, Tuple
from core.llm_interface import call_model

def trace_variable_flow(file: str = None, file_path: str = None, variable_name: Optional[str] = None, variable: Optional[str] = None) -> str:
    """
    Trace how variables flow through a Python file
    
    Args:
        file: Path to the Python file to analyze (alias for file_path)
        file_path: Path to the Python file to analyze
        variable_name: Specific variable to trace (alias for variable)
        variable: Specific variable to trace (if None, traces all variables)
    
    Returns:
        str: Analysis report of variable flow
    """
    # Handle parameter aliases
    if file and not file_path:
        file_path = file
    if variable and not variable_name:
        variable_name = variable
    
    if not file_path:
        return "Error: No file path provided"
    logging.info(f"Tracing variable flow in {file_path}")
    if variable_name:
        logging.info(f"Focusing on variable: {variable_name}")
    
    try:
        # Read and parse the file
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse the AST
        tree = ast.parse(source_code, filename=file_path)
        
        # Analyze variable flow
        analyzer = VariableFlowAnalyzer(variable_name)
        analyzer.visit(tree)
        
        # Generate report
        report = _generate_flow_report(analyzer, file_path, variable_name)
        
        # Enhance with LLM analysis if needed
        if len(analyzer.variables) > 0:
            enhanced_report = _enhance_with_llm_analysis(report, source_code, variable_name)
            return enhanced_report
        
        return report
        
    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        logging.error(error_msg)
        return error_msg
    except SyntaxError as e:
        error_msg = f"Syntax error in {file_path}: {e}"
        logging.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error tracing variable flow: {e}"
        logging.error(error_msg, exc_info=True)
        return error_msg

class VariableFlowAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze variable flow"""
    
    def __init__(self, target_variable: Optional[str] = None):
        self.target_variable = target_variable
        self.variables: Dict[str, List[Dict]] = {}
        self.current_function = None
        self.current_class = None
        self.line_number = 0
    
    def visit_FunctionDef(self, node):
        """Visit function definitions"""
        old_function = self.current_function
        self.current_function = node.name
        
        # Record function parameters as variable assignments
        for arg in node.args.args:
            self._record_variable(arg.arg, 'parameter', node.lineno, 
                                f"Function parameter in {node.name}")
        
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_ClassDef(self, node):
        """Visit class definitions"""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_Assign(self, node):
        """Visit assignment statements"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self._record_variable(target.id, 'assignment', node.lineno,
                                    f"Assigned in {self._get_context()}")
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        """Visit augmented assignment (+=, -=, etc.)"""
        if isinstance(node.target, ast.Name):
            self._record_variable(node.target.id, 'augmented_assignment', 
                                node.lineno, f"Modified in {self._get_context()}")
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Visit name references"""
        if isinstance(node.ctx, ast.Load):
            self._record_variable(node.id, 'reference', node.lineno,
                                f"Referenced in {self._get_context()}")
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Visit for loops"""
        if isinstance(node.target, ast.Name):
            self._record_variable(node.target.id, 'loop_variable', node.lineno,
                                f"Loop variable in {self._get_context()}")
        self.generic_visit(node)
    
    def visit_With(self, node):
        """Visit with statements"""
        for item in node.items:
            if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                self._record_variable(item.optional_vars.id, 'context_variable', 
                                    node.lineno, f"Context variable in {self._get_context()}")
        self.generic_visit(node)
    
    def _record_variable(self, var_name: str, usage_type: str, line_no: int, context: str):
        """Record a variable usage"""
        # If we're tracking a specific variable, only record that one
        if self.target_variable and var_name != self.target_variable:
            return
        
        if var_name not in self.variables:
            self.variables[var_name] = []
        
        self.variables[var_name].append({
            'type': usage_type,
            'line': line_no,
            'context': context,
            'function': self.current_function,
            'class': self.current_class
        })
    
    def _get_context(self) -> str:
        """Get current context string"""
        parts = []
        if self.current_class:
            parts.append(f"class {self.current_class}")
        if self.current_function:
            parts.append(f"function {self.current_function}")
        return " -> ".join(parts) if parts else "global scope"

def _generate_flow_report(analyzer: VariableFlowAnalyzer, file_path: str, 
                         target_variable: Optional[str]) -> str:
    """Generate a human-readable flow report"""
    if not analyzer.variables:
        return f"No variables found in {file_path}"
    
    report_lines = [
        f"Variable Flow Analysis for {file_path}",
        "=" * 50
    ]
    
    if target_variable:
        report_lines.append(f"Focusing on variable: {target_variable}")
        report_lines.append("")
    
    for var_name, usages in analyzer.variables.items():
        report_lines.append(f"Variable: {var_name}")
        report_lines.append("-" * 20)
        
        # Group usages by type
        usage_types = {}
        for usage in usages:
            usage_type = usage['type']
            if usage_type not in usage_types:
                usage_types[usage_type] = []
            usage_types[usage_type].append(usage)
        
        # Report each usage type
        for usage_type, type_usages in usage_types.items():
            report_lines.append(f"  {usage_type.replace('_', ' ').title()}:")
            for usage in type_usages:
                report_lines.append(f"    Line {usage['line']}: {usage['context']}")
        
        report_lines.append("")
    
    # Add summary
    total_vars = len(analyzer.variables)
    total_usages = sum(len(usages) for usages in analyzer.variables.values())
    report_lines.append(f"Summary: {total_vars} variables, {total_usages} total usages")
    
    return "\n".join(report_lines)

def _enhance_with_llm_analysis(report: str, source_code: str, 
                              target_variable: Optional[str]) -> str:
    """Enhance the report with LLM analysis"""
    try:
        focus = f" focusing on variable '{target_variable}'" if target_variable else ""
        
        prompt = f"""Analyze this variable flow report and source code{focus}:

VARIABLE FLOW REPORT:
{report}

SOURCE CODE:
{source_code[:2000]}...

Please provide insights about:
1. Potential issues with variable usage
2. Suggestions for improvement
3. Any patterns or anti-patterns you notice
4. Data flow concerns

Keep your analysis concise and actionable:"""

        llm_analysis = call_model(prompt, max_tokens=512, temperature=0.3)
        
        enhanced_report = f"""{report}

LLM Analysis:
{'-' * 20}
{llm_analysis}
"""
        return enhanced_report
        
    except Exception as e:
        logging.warning(f"Could not enhance report with LLM analysis: {e}")
        return report

def trace_function_calls(file_path: str, function_name: str) -> str:
    """
    Trace all calls to a specific function
    
    Args:
        file_path: Path to the Python file
        function_name: Name of the function to trace
    
    Returns:
        str: Report of function call locations and contexts
    """
    logging.info(f"Tracing calls to function '{function_name}' in {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code, filename=file_path)
        
        class FunctionCallTracer(ast.NodeVisitor):
            def __init__(self, target_func):
                self.target_func = target_func
                self.calls = []
                self.current_context = []
            
            def visit_FunctionDef(self, node):
                self.current_context.append(f"function {node.name}")
                self.generic_visit(node)
                self.current_context.pop()
            
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id == self.target_func:
                    context = " -> ".join(self.current_context) if self.current_context else "global"
                    self.calls.append({
                        'line': node.lineno,
                        'context': context,
                        'args': len(node.args)
                    })
                self.generic_visit(node)
        
        tracer = FunctionCallTracer(function_name)
        tracer.visit(tree)
        
        if not tracer.calls:
            return f"No calls to function '{function_name}' found in {file_path}"
        
        report_lines = [
            f"Function Call Trace for '{function_name}' in {file_path}",
            "=" * 50
        ]
        
        for call in tracer.calls:
            report_lines.append(f"Line {call['line']}: {call['context']} ({call['args']} args)")
        
        report_lines.append(f"\nTotal calls found: {len(tracer.calls)}")
        
        return "\n".join(report_lines)
        
    except Exception as e:
        error_msg = f"Error tracing function calls: {e}"
        logging.error(error_msg)
        return error_msg
