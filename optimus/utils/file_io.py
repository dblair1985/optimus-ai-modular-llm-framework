"""
File I/O Utility

This module provides safe file operations and utilities for the Optimus Bot.
"""

import os
import json
import logging
import shutil
from typing import Optional, Dict, Any, List
from pathlib import Path

def safe_read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read a file with error handling
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)
    
    Returns:
        str: File content or None if error
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        logging.debug(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except PermissionError:
        logging.error(f"Permission denied reading file: {file_path}")
        return None
    except UnicodeDecodeError:
        logging.error(f"Unicode decode error reading file: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading file {file_path}: {e}")
        return None

def safe_write_file(file_path: str, content: str, encoding: str = 'utf-8', 
                   backup: bool = True) -> bool:
    """
    Safely write content to a file with optional backup
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        encoding: File encoding (default: utf-8)
        backup: Whether to create a backup if file exists
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create backup if requested and file exists
        if backup and os.path.exists(file_path):
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
            logging.debug(f"Created backup: {backup_path}")
        
        # Write the file
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        logging.debug(f"Successfully wrote file: {file_path}")
        return True
        
    except PermissionError:
        logging.error(f"Permission denied writing file: {file_path}")
        return False
    except Exception as e:
        logging.error(f"Error writing file {file_path}: {e}")
        return False

def safe_read_json(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely read a JSON file
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        dict: Parsed JSON data or None if error
    """
    content = safe_read_file(file_path)
    if content is None:
        return None
    
    try:
        data = json.loads(content)
        logging.debug(f"Successfully parsed JSON from: {file_path}")
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in {file_path}: {e}")
        return None

def safe_write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """
    Safely write data to a JSON file
    
    Args:
        file_path: Path to the JSON file
        data: Data to write
        indent: JSON indentation (default: 2)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        json_content = json.dumps(data, indent=indent, ensure_ascii=False)
        return safe_write_file(file_path, json_content)
    except TypeError as e:
        logging.error(f"Error serializing data to JSON: {e}")
        return False

def ensure_directory(dir_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        dir_path: Path to the directory
    
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        logging.debug(f"Directory ensured: {dir_path}")
        return True
    except Exception as e:
        logging.error(f"Error creating directory {dir_path}: {e}")
        return False

def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a file
    
    Args:
        file_path: Path to the file
    
    Returns:
        dict: File information or None if error
    """
    try:
        stat = os.stat(file_path)
        path_obj = Path(file_path)
        
        return {
            'name': path_obj.name,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'extension': path_obj.suffix,
            'is_file': path_obj.is_file(),
            'is_dir': path_obj.is_dir(),
            'absolute_path': str(path_obj.absolute())
        }
    except Exception as e:
        logging.error(f"Error getting file info for {file_path}: {e}")
        return None

def find_files(directory: str, pattern: str = "*", recursive: bool = True) -> List[str]:
    """
    Find files matching a pattern
    
    Args:
        directory: Directory to search in
        pattern: File pattern to match (default: "*")
        recursive: Whether to search recursively
    
    Returns:
        list: List of matching file paths
    """
    try:
        path_obj = Path(directory)
        if not path_obj.exists():
            logging.warning(f"Directory does not exist: {directory}")
            return []
        
        if recursive:
            files = list(path_obj.rglob(pattern))
        else:
            files = list(path_obj.glob(pattern))
        
        # Convert to strings and filter out directories
        file_paths = [str(f) for f in files if f.is_file()]
        
        logging.debug(f"Found {len(file_paths)} files matching '{pattern}' in {directory}")
        return file_paths
        
    except Exception as e:
        logging.error(f"Error finding files in {directory}: {e}")
        return []

def copy_file(src: str, dst: str, overwrite: bool = False) -> bool:
    """
    Copy a file from source to destination
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not overwrite and os.path.exists(dst):
            logging.warning(f"Destination file exists and overwrite=False: {dst}")
            return False
        
        # Ensure destination directory exists
        ensure_directory(os.path.dirname(dst))
        
        shutil.copy2(src, dst)
        logging.debug(f"Copied file: {src} -> {dst}")
        return True
        
    except Exception as e:
        logging.error(f"Error copying file {src} to {dst}: {e}")
        return False

def move_file(src: str, dst: str, overwrite: bool = False) -> bool:
    """
    Move a file from source to destination
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not overwrite and os.path.exists(dst):
            logging.warning(f"Destination file exists and overwrite=False: {dst}")
            return False
        
        # Ensure destination directory exists
        ensure_directory(os.path.dirname(dst))
        
        shutil.move(src, dst)
        logging.debug(f"Moved file: {src} -> {dst}")
        return True
        
    except Exception as e:
        logging.error(f"Error moving file {src} to {dst}: {e}")
        return False

def delete_file(file_path: str, backup: bool = True) -> bool:
    """
    Delete a file with optional backup
    
    Args:
        file_path: Path to the file to delete
        backup: Whether to create a backup before deletion
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            logging.warning(f"File does not exist: {file_path}")
            return True  # Consider it successful if file doesn't exist
        
        if backup:
            backup_path = f"{file_path}.deleted"
            if copy_file(file_path, backup_path, overwrite=True):
                logging.debug(f"Created backup before deletion: {backup_path}")
        
        os.remove(file_path)
        logging.debug(f"Deleted file: {file_path}")
        return True
        
    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {e}")
        return False

def get_directory_size(directory: str) -> int:
    """
    Get the total size of a directory
    
    Args:
        directory: Path to the directory
    
    Returns:
        int: Total size in bytes, or 0 if error
    """
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    continue  # Skip files that can't be accessed
        
        return total_size
        
    except Exception as e:
        logging.error(f"Error calculating directory size for {directory}: {e}")
        return 0

def cleanup_temp_files(directory: str, pattern: str = "*.tmp") -> int:
    """
    Clean up temporary files in a directory
    
    Args:
        directory: Directory to clean
        pattern: Pattern for temp files (default: "*.tmp")
    
    Returns:
        int: Number of files deleted
    """
    try:
        temp_files = find_files(directory, pattern, recursive=True)
        deleted_count = 0
        
        for temp_file in temp_files:
            if delete_file(temp_file, backup=False):
                deleted_count += 1
        
        logging.info(f"Cleaned up {deleted_count} temporary files from {directory}")
        return deleted_count
        
    except Exception as e:
        logging.error(f"Error cleaning up temp files in {directory}: {e}")
        return 0
