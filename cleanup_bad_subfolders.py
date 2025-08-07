import os
import shutil

# === CONFIG ===
project_root = "/home/nvidia07/cat-breed-detector"
known_breeds = [
    "Abyssinian", "Bengal", "Birman", "Bombay", "British", "Egyptian",
    "Maine", "Persian", "Ragdoll", "Russian Blue", "Siamese", "Sphynx"
]

base_paths = [
    os.path.join(project_root, "data", "images", "train"),
    os.path.join(project_root, "data", "images", "val"),
    os.path.join(project_root, "data", "labels", "train"),
    os.path.join(project_root, "data", "labels", "val")
]

# === Delete unknown folders ===
for base in base_paths:
    for folder in os.listdir(base):
        folder_path = os.path.join(base, folder)
        if os.path.isdir(folder_path):
            if folder not in known_breeds:
                print(f"❌ Deleting: {folder_path}")
                shutil.rmtree(folder_path)
            else:
                print(f"✅ Keeping: {folder_path}")