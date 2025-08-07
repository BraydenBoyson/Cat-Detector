import os
import shutil
from collections import defaultdict

# Set paths
base_dir = "/home/nvidia07/cat-breed-detector"
images_dir = os.path.join(base_dir, "data/images")
labels_dir = os.path.join(base_dir, "data/labels")

threshold = 50  # Minimum instances required to keep a breed

# Count instances per breed
def count_instances(label_path):
    instance_counts = defaultdict(int)
    for split in ['train', 'val']:
        label_split_path = os.path.join(label_path, split)
        for breed in os.listdir(label_split_path):
            breed_path = os.path.join(label_split_path, breed)
            if not os.path.isdir(breed_path):
                continue
            for file in os.listdir(breed_path):
                if file.endswith(".txt"):
                    with open(os.path.join(breed_path, file), 'r') as f:
                        instance_counts[breed] += len(f.readlines())
    return instance_counts

# Remove breed folders if below threshold
def remove_low_instance_breeds(images_path, labels_path, instance_counts, threshold):
    for split in ['train', 'val']:
        for root_dir in [images_path, labels_path]:
            split_path = os.path.join(root_dir, split)
            for breed in os.listdir(split_path):
                breed_path = os.path.join(split_path, breed)
                if not os.path.isdir(breed_path):
                    continue
                if instance_counts.get(breed, 0) < threshold:
                    print(f"Removing breed '{breed}' (only {instance_counts.get(breed, 0)} instances)...")
                    shutil.rmtree(breed_path, ignore_errors=True)

# Run everything
if __name__ == "__main__":
    print("Counting breed instances...")
    counts = count_instances(labels_dir)
    print("\nRemoving breeds with fewer than", threshold, "instances...")
    remove_low_instance_breeds(images_dir, labels_dir, counts, threshold)
    print("\n✅ Cleanup complete.")