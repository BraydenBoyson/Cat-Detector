import os
import random

# Paths
BASE_DIR = os.path.expanduser('~/cat-breed-detector/data')
IMG_DIR = os.path.join(BASE_DIR, 'images')
LABEL_DIR = os.path.join(BASE_DIR, 'kitti_labels')
SPLIT_DIR = os.path.join(BASE_DIR, 'splits')
os.makedirs(SPLIT_DIR, exist_ok=True)

# Gather all image basenames that have corresponding label files
image_filenames = [
    f for f in os.listdir(IMG_DIR)
    if f.endswith(('.jpg', '.jpeg', '.png')) and os.path.exists(
        os.path.join(LABEL_DIR, os.path.splitext(f)[0] + '.txt')
    )
]

print(f"Total labeled images: {len(image_filenames)}")

# Shuffle and split
random.shuffle(image_filenames)
split_idx = int(0.8 * len(image_filenames))  # 80/20 train/val

train = image_filenames[:split_idx]
val = image_filenames[split_idx:]

# Save splits (without file extensions)
with open(os.path.join(SPLIT_DIR, 'train.txt'), 'w') as f:
    for fname in train:
        f.write(os.path.splitext(fname)[0] + '\n')

with open(os.path.join(SPLIT_DIR, 'val.txt'), 'w') as f:
    for fname in val:
        f.write(os.path.splitext(fname)[0] + '\n')

print("✅ Saved train/val splits to:", SPLIT_DIR)