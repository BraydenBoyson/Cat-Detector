import os
from collections import defaultdict

DATA_DIR = "/home/nvidia07/cat-breed-detector/data"
LABEL_DIR = os.path.join(DATA_DIR, "labels")

def count_instances():
    instance_counts = defaultdict(int)

    for split in ["train", "val"]:
        split_dir = os.path.join(LABEL_DIR, split)
        for breed in os.listdir(split_dir):
            breed_dir = os.path.join(split_dir, breed)
            if not os.path.isdir(breed_dir):
                continue

            for file in os.listdir(breed_dir):
                if file.endswith(".txt"):
                    file_path = os.path.join(breed_dir, file)
                    with open(file_path, "r") as f:
                        lines = f.readlines()
                        instance_counts[breed] += len(lines)

    return instance_counts

if __name__ == "__main__":
    counts = count_instances()
    print("\nClass Distribution:\n" + "-" * 20)
    for breed, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{breed}: {count} instances")