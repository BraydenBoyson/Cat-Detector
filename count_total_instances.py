import os
from collections import defaultdict

# Base label directory
LABEL_BASE = 'data/labels'  # Update if your path differs
splits = ['train', 'val']

# Count storage
class_counts = defaultdict(int)

# Count instances across splits
for split in splits:
    split_path = os.path.join(LABEL_BASE, split)
    print(f'Processing split: {split.upper()}')
    
    if not os.path.isdir(split_path):
        print(f'Skip missing split: {split_path}')
        continue

    for breed in os.listdir(split_path):
        breed_path = os.path.join(split_path, breed)
        if not os.path.isdir(breed_path):
            continue

        for label_file in os.listdir(breed_path):
            if not label_file.endswith('.txt'):
                continue
            label_path = os.path.join(breed_path, label_file)

            with open(label_path, 'r') as f:
                lines = f.readlines()
                class_counts[breed] += len(lines)

# Output results
print("\n🔢 Total Label Instance Count Per Breed (Train + Val):")
print("--------------------------------------------------------")
for breed, count in sorted(class_counts.items(), key=lambda x: -x[1]):
    print(f"{breed}: {count} instances")