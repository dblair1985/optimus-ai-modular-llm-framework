import os
import json
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "model_path": "/path/to/local/mistral/model",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "max_tokens": 512,
    "temperature": 0.7,
    "memory_path": "data/memory.json",
    "code_map_path": "data/code_map.json"
}

def load_config():
    """Load configuration from environment variables or defaults"""
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if available
    if "MODEL_PATH" in os.environ:
        config["model_path"] = os.environ["MODEL_PATH"]
    
    if "EMBEDDING_MODEL" in os.environ:
        config["embedding_model"] = os.environ["EMBEDDING_MODEL"]
    
    return config

def get_config():
    """Get the current configuration"""
    return load_config()

# Module-level constants
MODEL_PATH = load_config()["model_path"]
EMBEDDING_MODEL = load_config()["embedding_model"]
