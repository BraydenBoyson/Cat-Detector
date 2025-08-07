import os
import shutil
import random
from pathlib import Path

# === Paths ===
project_root = "/home/nvidia07/cat-breed-detector"
undo_dir = os.path.join(project_root, "undo_roboflow")

# Where to restore
images_root = os.path.join(project_root, "data", "images")
labels_root = os.path.join(project_root, "data", "labels")

# Known breeds (original ones, format-sensitive)
known_breeds = [
    "Abyssinian", "Bengal", "Birman", "Bombay", "British", "Egyptian",
    "Maine", "Persian", "Ragdoll", "Russian Blue", "Siamese", "Sphynx"
]

# Create all breed subfolders (train/val)
for base in [images_root, labels_root]:
    for split in ["train", "val"]:
        for breed in known_breeds:
            os.makedirs(os.path.join(base, split, breed), exist_ok=True)

# Collect all images from undo folder
image_exts = (".jpg", ".jpeg", ".png")
images = [f for f in os.listdir(undo_dir) if f.lower().endswith(image_exts)]
random.shuffle(images)

# 80/20 split
split_index = int(len(images) * 0.8)

for i, img_file in enumerate(images):
    img_path = os.path.join(undo_dir, img_file)
    base_name = os.path.splitext(img_file)[0]
    label_file = base_name + ".txt"
    label_path = os.path.join(undo_dir, label_file)

    # Guess the breed based on file name
    matched_breed = None
    for breed in known_breeds:
        normalized_breed = breed.replace(" ", "").lower()
        if normalized_breed in base_name.lower():
            matched_breed = breed
            break

    if not matched_breed:
        print(f"❌ Skipping unrecognized breed: {img_file}")
        continue

    # Decide split
    split = "train" if i < split_index else "val"

    # Target folders
    img_dst = os.path.join(images_root, split, matched_breed, img_file)
    lbl_dst = os.path.join(labels_root, split, matched_breed, label_file)

    # Move files
    shutil.move(img_path, img_dst)
    if os.path.exists(label_path):
        shutil.move(label_path, lbl_dst)
        print(f"✅ Restored {img_file} and {label_file} to {split}/{matched_breed}")
    else:
        print(f"⚠️ Image {img_file} moved, but no label found.")