import os
import shutil

base_dirs = [
    "/home/nvidia07/cat-breed-detector/data/images/train",
    "/home/nvidia07/cat-breed-detector/data/images/val",
    "/home/nvidia07/cat-breed-detector/data/labels/train",
    "/home/nvidia07/cat-breed-detector/data/labels/val"
]

# Utility: Delete empty folders
def delete_if_empty(path):
    if os.path.exists(path) and len(os.listdir(path)) == 0:
        shutil.rmtree(path)
        print(f"🗑️ Deleted empty folder: {path}")

# Utility: Move contents from src to dst
def move_contents(src, dst):
    if not os.path.exists(src):
        return
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        shutil.move(os.path.join(src, f), os.path.join(dst, f))
    shutil.rmtree(src)
    print(f"📦 Moved contents from {src} to {dst}")

# Pass 1: Move everything from 'Abyssianian' → 'Abyssinian'
for base in base_dirs:
    wrong = os.path.join(base, "Abyssianian")
    correct = os.path.join(base, "Abyssinian")
    move_contents(wrong, correct)

# Pass 2: Delete duplicate folders with underscores (if proper one exists)
for base in base_dirs:
    for folder in os.listdir(base):
        folder_path = os.path.join(base, folder)

        # Only check folders with underscores
        if "_" in folder:
            spaced_name = folder.replace("_", " ")
            spaced_path = os.path.join(base, spaced_name)

            if os.path.exists(spaced_path):
                # Move files before deleting just in case
                move_contents(folder_path, spaced_path)

# Pass 3: Delete empty folders
for base in base_dirs:
    for folder in os.listdir(base):
        folder_path = os.path.join(base, folder)
        delete_if_empty(folder_path)

print("\n✅ Cleanup complete.")