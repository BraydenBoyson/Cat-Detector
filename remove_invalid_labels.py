import os

# Constants
LABEL_DIRS = [
    "/home/nvidia07/cat-breed-detector/data/labels/train",
    "/home/nvidia07/cat-breed-detector/data/labels/val",
]
NUM_CLASSES = 44  # valid class indices: 0 through 43

def is_invalid_label(file_path):
    with open(file_path, "r") as f:
        for line in f:
            try:
                class_idx = int(line.strip().split()[0])
                if class_idx >= NUM_CLASSES:
                    return True
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                return True  # treat corrupt lines as invalid
    return False

def clean_labels():
    total_deleted = 0
    for label_dir in LABEL_DIRS:
        for root, _, files in os.walk(label_dir):
            for file in files:
                if file.endswith(".txt"):
                    full_path = os.path.join(root, file)
                    if is_invalid_label(full_path):
                        print(f"❌ Deleting invalid label file: {full_path}")
                        os.remove(full_path)
                        total_deleted += 1
    print(f"\n✅ Deleted {total_deleted} invalid label files.")

if __name__ == "__main__":
    clean_labels()