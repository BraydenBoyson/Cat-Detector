import os
import shutil

# Set the base directory
base_dir = '/home/nvidia07/cat-breed-detector/data'

# Split types
splits = ['train', 'val']

for split in splits:
    img_split_dir = os.path.join(base_dir, 'images', split)
    lbl_split_dir = os.path.join(base_dir, 'labels', split)

    # Make sure the paths exist
    if not os.path.exists(img_split_dir) or not os.path.exists(lbl_split_dir):
        print(f"Missing path: {img_split_dir} or {lbl_split_dir}")
        continue

    # List all files in the images split directory recursively
    for root, _, files in os.walk(img_split_dir):
        for file in files:
            if not file.lower().endswith('.jpg'):
                continue

            # Extract breed from filename
            breed = file.split('_')[0]

            # Define source paths
            img_path = os.path.join(root, file)
            label_name = file.replace('.jpg', '.txt')
            lbl_path = os.path.join(lbl_split_dir, label_name)

            # Define destination directories
            dst_img_dir = os.path.join(img_split_dir, breed)
            dst_lbl_dir = os.path.join(lbl_split_dir, breed)

            os.makedirs(dst_img_dir, exist_ok=True)
            os.makedirs(dst_lbl_dir, exist_ok=True)

            # Move image
            dst_img_path = os.path.join(dst_img_dir, file)
            if not os.path.exists(dst_img_path):
                shutil.move(img_path, dst_img_path)

            # Move label if it exists
            if os.path.exists(lbl_path):
                dst_lbl_path = os.path.join(dst_lbl_dir, label_name)
                if not os.path.exists(dst_lbl_path):
                    shutil.move(lbl_path, dst_lbl_path)
            else:
                print(f"⚠️ Warning: Label not found for {file}")