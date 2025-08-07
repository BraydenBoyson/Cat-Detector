import os
import shutil
import random

# Paths
src_dir = "/home/nvidia07/cat-breed-detector/data/images"
train_dir = "/home/nvidia07/cat-breed-detector/data/images/train"
val_dir = "/home/nvidia07/cat-breed-detector/data/images/val"

# Make sure output directories exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# List all images
images = [f for f in os.listdir(src_dir) if f.endswith(".jpg")]

# Shuffle for randomness
random.shuffle(images)

# Split 80% train, 20% val
split_idx = int(len(images) * 0.8)
train_images = images[:split_idx]
val_images = images[split_idx:]

# Copy train images
for img in train_images:
    shutil.copy(os.path.join(src_dir, img), os.path.join(train_dir, img))

# Copy val images
for img in val_images:
    shutil.copy(os.path.join(src_dir, img), os.path.join(val_dir, img))

print(f"Copied {len(train_images)} images to train/")
print(f"Copied {len(val_images)} images to val/")