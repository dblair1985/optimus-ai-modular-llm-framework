# File: C:/Omega/Optimus/create_optimus.py

import os

folders = [
    "core", "engine", "skills", "gui/tabs", "models", "memory", "utils"
]

files = [
    "config.json", "main.py", "requirements.txt", "README.md"
]

starter_files = {
    "README.md": "# Optimus (DaveBot V2)\nModular AI Assistant Framework.",
    "requirements.txt": "tkinter\nsentence-transformers\nllama-cpp-python\nchromadb\n",
    "config.json": "{\n  \"model_path\": \"models/mistral.gguf\",\n  \"memory_top_k\": 5\n}"
}

print("🛠️ Building file structure...")

for folder in folders:
    path = os.path.join(os.getcwd(), folder)
    os.makedirs(path, exist_ok=True)
    print(f"📂 {path}")

for file, content in starter_files.items():
    with open(file, "w") as f:
        f.write(content)
    print(f"📄 Created {file}")

print("✅ File scaffold generated.")
