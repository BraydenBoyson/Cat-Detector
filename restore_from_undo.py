import os
import shutil

# === CONFIG ===
project_root = "/home/nvidia07/cat-breed-detector"
undo_dir = os.path.join(project_root, "undo_roboflow")

# Your known breeds
known_breeds = [
    "Abyssinian", "Bengal", "Birman", "Bombay", "British", "Egyptian",
    "Maine", "Persian", "Ragdoll", "Russian Blue", "Siamese", "Sphynx"
]

# === Restore each file ===
for filename in os.listdir(undo_dir):
    filepath = os.path.join(undo_dir, filename)

    # Determine split and type
    split = "train" if "train" in filename.lower() else "val"  # crude heuristic
    dtype = "images" if filename.endswith((".jpg", ".jpeg", ".png")) else "labels"

    # Match breed name from filename
    matched_breed = None
    for breed in known_breeds:
        if filename.replace(" ", "_").startswith(breed.replace(" ", "_")):
            matched_breed = breed
            break

    if not matched_breed:
        print(f"❌ Unknown breed in filename: {filename}")
        continue

    target_folder = os.path.join(project_root, "data", dtype, split, matched_breed)
    os.makedirs(target_folder, exist_ok=True)

    dst = os.path.join(target_folder, filename)

    shutil.move(filepath, dst)
    print(f"✅ Restored {filename} -> {target_folder}")