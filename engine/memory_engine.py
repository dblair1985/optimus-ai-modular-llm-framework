# File: C:/Omega/Optimus/engine/memory_engine.py

import json
import os

MEMORY_PATH = "memory/memory_index.json"

def load_memory_index():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return []

def semantic_search(query, memory, top_k=5):
    return memory[:top_k]  # Placeholder, upgrade with embedding search later
