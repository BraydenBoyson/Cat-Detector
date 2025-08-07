import os
from pathlib import Path
import shutil

# Configuration
LABEL_DIRS = [
    '/home/nvidia07/cat-breed-detector/data/labels/train/Abyssinian',
    '/home/nvidia07/cat-breed-detector/data/labels/val/Abyssinian',
]
IMAGE_DIRS = [
    '/home/nvidia07/cat-breed-detector/data/images/train/Abyssinian',
    '/home/nvidia07/cat-breed-detector/data/images/val/Abyssinian',
]
CLASS_ID = '0'  # Class ID for Abyssinian
MAX_INSTANCES = 250
SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png', '.bmp']

def count_abyssinian_in_file(filepath):
    with open(filepath, 'r') as f:
        return sum(1 for line in f if line.startswith(CLASS_ID + ' '))

def remove_file_and_image(label_path, image_folder):
    basename = label_path.stem
    # Remove label
    label_path.unlink(missing_ok=True)
    # Remove corresponding image
    for ext in SUPPORTED_EXTS:
        image_path = image_folder / (basename + ext)
        if image_path.exists():
            image_path.unlink()
            break

def process_folder(label_dir, image_dir, class_id, max_instances, running_total):
    label_dir = Path(label_dir)
    image_dir = Path(image_dir)
    files = sorted(label_dir.glob('*.txt'))

    for label_file in files:
        instance_count = count_abyssinian_in_file(label_file)
        if running_total + instance_count <= max_instances:
            running_total += instance_count
        else:
            remove_file_and_image(label_file, image_dir)

    return running_total

def main():
    running_total = 0
    for label_dir, image_dir in zip(LABEL_DIRS, IMAGE_DIRS):
        running_total = process_folder(label_dir, image_dir, CLASS_ID, MAX_INSTANCES, running_total)

    print(f'✅ Final Abyssinian instance count limited to {running_total}')

if __name__ == '__main__':
    main()