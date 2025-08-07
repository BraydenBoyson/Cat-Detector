import os
import random

# Set the base directories
images_dir = "/home/nvidia07/cat-breed-detector/data/images/train"
labels_dir = "/home/nvidia07/cat-breed-detector/data/labels/train"
INSTANCE_LIMIT = 150

def trim_breed(breed_name):
    label_breed_dir = os.path.join(labels_dir, breed_name)
    image_breed_dir = os.path.join(images_dir, breed_name)

    if not os.path.exists(label_breed_dir) or not os.path.exists(image_breed_dir):
        print(f"⚠️ Skipping {breed_name} — folder missing.")
        return

    # Get all label files (assumes YOLO format: one instance per line in .txt files)
    label_files = [f for f in os.listdir(label_breed_dir) if f.endswith(".txt")]
    instance_count = 0
    label_file_map = {}

    # Count all instances
    for file in label_files:
        path = os.path.join(label_breed_dir, file)
        with open(path, "r") as f:
            lines = f.readlines()
            count = len(lines)
            instance_count += count
            label_file_map[file] = count

    print(f"{breed_name}: {instance_count} instances")

    if instance_count <= INSTANCE_LIMIT:
        print(f"✅ {breed_name} is within the limit.\n")
        return

    # Randomize label files and start trimming
    to_delete = []
    current_total = instance_count

    shuffled = list(label_file_map.items())
    random.shuffle(shuffled)

    for file_name, count in shuffled:
        if current_total <= INSTANCE_LIMIT:
            break
        to_delete.append(file_name)
        current_total -= count

    print(f"⚠️ Trimming {breed_name}: removing {len(to_delete)} files to reach {INSTANCE_LIMIT} instances.")

    for file_name in to_delete:
        label_path = os.path.join(label_breed_dir, file_name)
        image_name = os.path.splitext(file_name)[0] + ".jpg"
        image_path = os.path.join(image_breed_dir, image_name)

        if os.path.exists(label_path):
            os.remove(label_path)
        if os.path.exists(image_path):
            os.remove(image_path)

    print(f"✅ Trimmed {breed_name} to ~{INSTANCE_LIMIT} instances.\n")

# Main
if __name__ == "__main__":
    breeds = os.listdir(labels_dir)
    breeds.sort()
    for breed in breeds:
        trim_breed(breed)