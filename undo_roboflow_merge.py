
import os
import shutil

# === CONFIG ===
project_root = "/home/nvidia07/cat-breed-detector"
undo_dir = os.path.join(project_root, "undo_roboflow")
os.makedirs(undo_dir, exist_ok=True)

paths = [
    os.path.join(project_root, "data", "images", "train"),
    os.path.join(project_root, "data", "images", "val"),
    os.path.join(project_root, "data", "labels", "train"),
    os.path.join(project_root, "data", "labels", "val")
]

for base in paths:
    for breed in os.listdir(base):
        breed_path = os.path.join(base, breed)
        if not os.path.isdir(breed_path):
            continue

        for file in os.listdir(breed_path):
            file_path = os.path.join(breed_path, file)
            if os.path.isfile(file_path):
                undo_target = os.path.join(undo_dir, file)
                shutil.move(file_path, undo_target)
                print(f"Moved back: {file_path} -> {undo_target}")
