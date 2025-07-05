# File: C:/Omega/Optimus/core/handler.py

from engine.llm_runner import ask_llm
from engine.memory_engine import load_memory_index, semantic_search
from skills.skill_router import run_skill
from core.self_patch_engine import self_patch_check


def process_input(user_input):
    if user_input.startswith("!run "):
        return run_skill(user_input[5:])

    memory = load_memory_index()
    memory_hits = semantic_search(user_input, memory)

    context = "\n".join([hit.get("chunk", "") for hit in memory_hits])

    prompt = f"Context:\n{context}\n\nUser: {user_input}\nAssistant:"
    response = ask_llm(prompt)

    self_patch_check()

    return response
