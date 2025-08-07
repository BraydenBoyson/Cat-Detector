import os
from pathlib import Path

# ✅ Set correct paths
label_dirs = [
    "/home/nvidia07/cat-breed-detector/data/labels/train",
    "/home/nvidia07/cat-breed-detector/data/labels/val"
]

# ✅ YOLO class range is 0 to 43 (44 total classes)
max_class_index = 43

def is_label_valid(label_path):
    try:
        with open(label_path, "r") as f:
            for line in f:
                class_index = int(line.strip().split()[0])
                if class_index > max_class_index:
                    return False
        return True
    except:
        return False

# 🧹 Delete invalid labels
deleted = 0
for label_dir in label_dirs:
    for label_file in Path(label_dir).rglob("*.txt"):
        if not is_label_valid(label_file):
            os.remove(label_file)
            deleted += 1
            print(f"Deleted invalid label: {label_file}")

print(f"\n✅ Done. Deleted {deleted} invalid label files.")