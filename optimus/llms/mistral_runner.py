import logging
from typing import Optional

try:
    from ctransformers import AutoModelForCausalLM
    CTRANSFORMERS_AVAILABLE = True
except ImportError:
    CTRANSFORMERS_AVAILABLE = False
    logging.warning("ctransformers not available. Install with: pip install ctransformers")

class MistralLLM:
    """Local Mistral LLM runner using ctransformers"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model: Optional[AutoModelForCausalLM] = None
        self._load_model()
    
    def _load_model(self):
        """Load the Mistral model"""
        if not CTRANSFORMERS_AVAILABLE:
            raise ImportError("ctransformers is required but not installed")
        
        try:
            logging.info(f"Loading Mistral model from {self.model_path}")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                model_type="mistral",
                gpu_layers=0  # Use CPU by default
            )
            logging.info("Mistral model loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load Mistral model: {e}")
            # Fallback to mock model for development
            self.model = None
    
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """Generate text using the Mistral model"""
        if self.model is None:
            # Fallback response for development/testing
            logging.warning("Model not loaded, returning mock response")
            return self._mock_response(prompt)
        
        try:
            response = self.model(
                prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "\n\n"]
            )
            return response.strip()
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        """Mock response for development when model is not available"""
        if "plan" in prompt.lower() or "steps" in prompt.lower():
            return '''[
    {"action": "generate_task_code", "params": {"task": "improve error handling"}},
    {"action": "trace_variable_flow", "params": {"file": "patch_engine.py"}}
]'''
        return "This is a mock response from Mistral LLM. Please configure a valid model path."
    
    def is_available(self) -> bool:
        """Check if the model is available and loaded"""
        return self.model is not None
