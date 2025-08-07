import os
import shutil

# Paths
images_val_dir = "data/images/val"
labels_train_dir = "data/labels/train"
labels_val_dir = "data/labels/val"

os.makedirs(labels_val_dir, exist_ok=True)

# For each image in val folder, copy matching label file from train labels
val_images = [f for f in os.listdir(images_val_dir) if f.endswith('.jpg')]

copied = 0
for img_file in val_images:
    label_file = img_file.replace('.jpg', '.txt')
    src_label = os.path.join(labels_train_dir, label_file)
    dst_label = os.path.join(labels_val_dir, label_file)
    if os.path.exists(src_label):
        shutil.copy(src_label, dst_label)
        copied += 1
    else:
        print(f"Warning: label file not found for {img_file}")

print(f"Copied {copied} label files to {labels_val_dir}")