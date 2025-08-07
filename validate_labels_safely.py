import os
from pathlib import Path
import shutil

# Setup
label_dirs = [
    "/home/nvidia07/cat-breed-detector/data/labels/train",
    "/home/nvidia07/cat-breed-detector/data/labels/val"
]
max_class_index = 43
backup_dir = "/home/nvidia07/cat-breed-detector/label_backups"

# Make backup folder
os.makedirs(backup_dir, exist_ok=True)

# Check and optionally clean
invalid_labels = []

for label_dir in label_dirs:
    for label_file in Path(label_dir).rglob("*.txt"):
        with open(label_file, "r") as f:
            lines = f.readlines()
        for line in lines:
            try:
                class_idx = int(line.strip().split()[0])
                if class_idx > max_class_index:
                    invalid_labels.append(str(label_file))
                    break
            except:
                continue

# Show what will be deleted
if not invalid_labels:
    print("✅ No invalid labels found.")
else:
    print("⚠️ Found label files with invalid class indices:")
    for f in invalid_labels:
        print(f" - {f}")

    confirm = input("\nDo you want to delete these label files and back them up? (y/n): ").strip().lower()
    if confirm == 'y':
        for file in invalid_labels:
            # Back up before deleting
            dest = Path(backup_dir) / Path(file).name
            shutil.copy(file, dest)
            os.remove(file)
            print(f"Deleted and backed up: {file}")
        print("\n✅ Done.")
    else:
        print("❌ No files deleted.")