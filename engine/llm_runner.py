# File: C:/Omega/Optimus/engine/llm_runner.py

from llama_cpp import Llama

llm = Llama(
    model_path="models/mistral.gguf",
    n_ctx=8192,
    n_gpu_layers=999
)

def ask_llm(prompt):
    result = llm(
        prompt=prompt,
        max_tokens=1024,
        temperature=0.2,
        stop=["</s>"]
    )
    return result["choices"][0]["text"].strip()
