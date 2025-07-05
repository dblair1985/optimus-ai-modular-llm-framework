import logging
from llms.mistral_runner import MistralLLM
from config.settings import MODEL_PATH, get_config

# Global LLM instance
_llm = None

def get_llm():
    """Get or create the LLM instance"""
    global _llm
    if _llm is None:
        config = get_config()
        _llm = MistralLLM(config["model_path"])
    return _llm

def call_model(prompt: str, max_tokens: int = None, temperature: float = None) -> str:
    """Call the model with the given prompt"""
    config = get_config()
    
    # Use config defaults if not specified
    if max_tokens is None:
        max_tokens = config.get("max_tokens", 512)
    if temperature is None:
        temperature = config.get("temperature", 0.7)
    
    try:
        llm = get_llm()
        response = llm.generate(prompt, max_tokens=max_tokens, temperature=temperature)
        logging.debug(f"LLM response: {response[:100]}...")
        return response
    except Exception as e:
        logging.error(f"Error calling model: {e}")
        return "Error: Unable to generate response"

def is_model_available() -> bool:
    """Check if the model is available"""
    try:
        llm = get_llm()
        return llm.is_available()
    except Exception:
        return False
