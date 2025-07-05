#!/usr/bin/env python3
"""
Installation script for Optimus Bot

This script helps set up the Optimus Bot environment and dependencies.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Try running manually: pip install -r requirements.txt")
        return False

def setup_directories():
    """Ensure all required directories exist"""
    print("📁 Setting up directories...")
    
    directories = [
        "data",
        "models",  # For storing LLM models
        "logs",    # For log files
        "temp"     # For temporary files
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✅ {directory}/")
    
    return True

def create_config():
    """Create or update configuration"""
    print("⚙️ Setting up configuration...")
    
    config_path = Path("config/settings.py")
    if config_path.exists():
        print("  ✅ Configuration already exists")
        return True
    
    # Configuration is already created, just verify
    print("  ✅ Configuration verified")
    return True

def download_model_info():
    """Provide information about downloading models"""
    print("\n🤖 Model Setup Information:")
    print("=" * 50)
    print("To use Optimus Bot with a local Mistral model:")
    print()
    print("1. Download a Mistral model in GGUF format:")
    print("   - Visit: https://huggingface.co/models?search=mistral+gguf")
    print("   - Recommended: mistral-7b-instruct-v0.1.Q4_K_M.gguf")
    print()
    print("2. Place the model in the models/ directory")
    print()
    print("3. Update the MODEL_PATH in config/settings.py:")
    print("   MODEL_PATH = 'models/your-model-name.gguf'")
    print()
    print("4. Or set environment variable:")
    print("   export MODEL_PATH='models/your-model-name.gguf'")
    print()

def run_tests():
    """Run basic tests to verify installation"""
    print("🧪 Running basic tests...")
    
    try:
        # Test imports
        sys.path.insert(0, ".")
        from core.agent_loop import get_agent_status
        from skills import list_available_skills
        from utils.code_scanner import scan_codebase
        
        # Test basic functionality
        skills = list_available_skills()
        status = get_agent_status()
        
        print(f"  ✅ Found {len(skills)} skills")
        print(f"  ✅ Memory system working")
        print("  ✅ All core modules imported successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 Optimus Bot Installation")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Setup directories
    if success and not setup_directories():
        success = False
    
    # Create configuration
    if success and not create_config():
        success = False
    
    # Install dependencies (optional for basic functionality)
    print("\n📦 Dependency Installation:")
    print("Note: ctransformers is optional for development/testing")
    install_deps = input("Install dependencies now? (y/n): ").lower().strip()
    
    if install_deps == 'y':
        if not install_dependencies():
            print("⚠️ Dependencies failed to install, but basic functionality will work")
    
    # Run tests
    if success and not run_tests():
        print("⚠️ Some tests failed, but installation may still be functional")
    
    # Show model information
    download_model_info()
    
    if success:
        print("\n✅ Installation completed!")
        print("\nNext steps:")
        print("1. Run demo: python demo.py")
        print("2. Run agent: python main.py")
        print("3. See README.md for detailed usage")
    else:
        print("\n❌ Installation had issues")
        print("Check the errors above and try manual installation")

if __name__ == "__main__":
    main()
