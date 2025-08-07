import os
import shutil
import random

# === CONFIG ===
project_root = "/home/nvidia07/cat-breed-detector"
undo_dir = os.path.join(project_root, "undo_roboflow")

# Your known breeds
known_breeds = [
    "Abyssinian", "Bengal", "Birman", "Bombay", "British", "Egyptian",
    "Maine", "Persian", "Ragdoll", "Russian Blue", "Siamese", "Sphynx"
]

# Create destination structure if needed
for breed in known_breeds:
    for dtype in ["images", "labels"]:
        for split in ["train", "val"]:
            os.makedirs(os.path.join(project_root, "data", dtype, split, breed), exist_ok=True)

# Go through undo folder and restore files
all_files = os.listdir(undo_dir)
random.shuffle(all_files)  # randomize

for i, filename in enumerate(all_files):
    filepath = os.path.join(undo_dir, filename)

    # Determine type
    dtype = "images" if filename.endswith((".jpg", ".jpeg", ".png")) else "labels"

    # Try to match breed from filename
    matched_breed = None
    for breed in known_breeds:
        if filename.replace(" ", "_").startswith(breed.replace(" ", "_")):
            matched_breed = breed
            break

    if not matched_breed:
        print(f"❌ Skipping unknown breed: {filename}")
        continue

    # 80% train, 20% val split
    split = "train" if i < len(all_files) * 0.8 else "val"

    # Move file
    target_path = os.path.join(project_root, "data", dtype, split, matched_breed)
    os.makedirs(target_path, exist_ok=True)
    shutil.move(filepath, os.path.join(target_path, filename))
    print(f"✅ Restored: {filename} -> {dtype}/{split}/{matched_breed}")