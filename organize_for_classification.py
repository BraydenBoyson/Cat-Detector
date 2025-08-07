import os
import shutil

# Path base
base_path = "/home/nvidia07/cat-breed-detector/data"

# The splits to process
splits = ["train", "val", "images"]

# Replace this dictionary with your actual class id to breed name mapping
class_id_to_breed = {
    "0": "abyssinian",
    "1": "bengal",
    "2": "birman",
    "3": "british_shorthair",
    "4": "egyptian_mau",
    "5": "maine_coon",
    "6": "persian",
    "7": "ragdoll",
    "8": "russian_blue",
    "9": "siamese",
    "10": "sphynx"
}

for split in splits:
    images_dir = os.path.join(base_path, "images", split)
    labels_dir = os.path.join(base_path, "labels", split)

    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        print(f"Skipping split '{split}' because folder does not exist.")
        continue

    for filename in os.listdir(labels_dir):
        if not filename.endswith(".txt"):
            continue

        label_path = os.path.join(labels_dir, filename)
        image_name = filename.replace(".txt", ".jpg")
        image_path = os.path.join(images_dir, image_name)

        if not os.path.exists(image_path):
            print(f"Image {image_path} not found, skipping.")
            continue

        with open(label_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            print(f"No labels found in {label_path}, skipping.")
            continue

        # Assuming single class per image (if multiple, you can adapt this)
        class_id = lines[0].strip().split()[0]
        breed_name = class_id_to_breed.get(class_id, "unknown")

        breed_folder = os.path.join(images_dir, breed_name)
        os.makedirs(breed_folder, exist_ok=True)

        dest_path = os.path.join(breed_folder, image_name)
        print(f"Moving {image_path} to {dest_path}")
        shutil.move(image_path, dest_path)