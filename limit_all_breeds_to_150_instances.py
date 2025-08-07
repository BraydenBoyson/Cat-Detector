import os
import random

DATA_DIR = "/home/nvidia07/cat-breed-detector/data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
LABEL_DIR = os.path.join(DATA_DIR, "labels")

MAX_INSTANCES = 150
SPLITS = ["train", "val"]

def get_label_path(image_path):
    return image_path.replace("/images/", "/labels/").replace(".jpg", ".txt").replace(".png", ".txt")

def count_instances_for_breed(breed):
    total = 0
    file_map = []

    for split in SPLITS:
        label_dir = os.path.join(LABEL_DIR, split, breed)
        image_dir = os.path.join(IMAGE_DIR, split, breed)

        if not os.path.isdir(label_dir):
            continue

        for fname in os.listdir(label_dir):
            if not fname.endswith(".txt"):
                continue
            fpath = os.path.join(label_dir, fname)
            with open(fpath, "r") as f:
                lines = f.readlines()
            total += len(lines)
            file_map.append({
                "label_path": fpath,
                "image_path": os.path.join(image_dir, fname.replace(".txt", ".jpg")),
                "count": len(lines),
                "split": split
            })

    return total, file_map

def trim_breed(breed):
    total_instances, files = count_instances_for_breed(breed)

    if total_instances <= MAX_INSTANCES:
        print(f"✅ {breed} already within limit ({total_instances} instances).")
        return

    print(f"⚠️ Trimming {breed}: {total_instances} → {MAX_INSTANCES} instances...")

    # Randomly shuffle to avoid always trimming same files
    random.shuffle(files)

    current_total = total_instances
    for item in files:
        if current_total <= MAX_INSTANCES:
            break
        if not os.path.exists(item["label_path"]):
            continue

        # Read label file
        with open(item["label_path"], "r") as f:
            lines = f.readlines()

        if len(lines) <= (current_total - MAX_INSTANCES):
            # Delete whole file (label + image)
            os.remove(item["label_path"])
            if os.path.exists(item["image_path"]):
                os.remove(item["image_path"])
            current_total -= len(lines)
        else:
            # Trim the label file instead of deleting it completely
            lines_to_keep = len(lines) - (current_total - MAX_INSTANCES)
            with open(item["label_path"], "w") as f:
                f.writelines(lines[:lines_to_keep])
            current_total = MAX_INSTANCES

    print(f"✅ {breed} trimmed to {MAX_INSTANCES} instances.")

def main():
    print("📦 Trimming all breeds to max 150 instances (across train + val)...\n")
    label_train_dir = os.path.join(LABEL_DIR, "train")
    breeds = [d for d in os.listdir(label_train_dir) if os.path.isdir(os.path.join(label_train_dir, d))]

    for breed in sorted(breeds):
        trim_breed(breed)

if __name__ == "__main__":
    main()
    