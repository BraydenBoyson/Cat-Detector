import os
import shutil
import csv

# Paths
base_path = "/home/nvidia07/cat-breed-detector/data"
image_folders = ['images/train', 'images/val']
label_folders = ['labels/train', 'labels/val']

# CSV file that maps image filename to breed
csv_file = "/home/nvidia07/cat-breed-detector/image_breeds.csv"

# Read mapping of filename -> breed
filename_to_breed = {}
with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename_to_breed[row['filename']] = row['breed']

# All breeds (you can also extract from CSV dynamically)
breeds = [
    'abyssinian', 'bengal', 'birman', 'british_shorthair', 'egyptian_mau', 
    'maine_coon', 'persian', 'ragdoll', 'russian_blue', 'siamese', 'sphynx'
]

def organize(folder_type):
    images_dir = os.path.join(base_path, 'images', folder_type)
    labels_dir = os.path.join(base_path, 'labels', folder_type)
    
    for breed in breeds:
        # Create breed subfolders in images and labels folders
        os.makedirs(os.path.join(images_dir, breed), exist_ok=True)
        os.makedirs(os.path.join(labels_dir, breed), exist_ok=True)
    
    # Iterate over images in this folder
    for img_name in os.listdir(images_dir):
        img_path = os.path.join(images_dir, img_name)
        if not os.path.isfile(img_path):
            continue
        if img_name not in filename_to_breed:
            print(f"Warning: {img_name} not found in breed mapping CSV, skipping.")
            continue
        
        breed = filename_to_breed[img_name]
        if breed not in breeds:
            print(f"Warning: Breed '{breed}' for {img_name} not recognized, skipping.")
            continue
        
        # Move image
        new_img_path = os.path.join(images_dir, breed, img_name)
        shutil.move(img_path, new_img_path)
        
        # Move corresponding label file if exists
        label_name = os.path.splitext(img_name)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_name)
        if os.path.exists(label_path):
            new_label_path = os.path.join(labels_dir, breed, label_name)
            shutil.move(label_path, new_label_path)
        else:
            print(f"Label file {label_name} not found for image {img_name}.")

print("Organizing training images and labels...")
organize('train')

print("Organizing validation images and labels...")
organize('val')

print("Done!")