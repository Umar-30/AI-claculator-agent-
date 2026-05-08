import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_message(role, content):
    memory = load_memory()
    memory.append({
        "role": role,
        "content": content
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def get_memory():
    return load_memory()

def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
