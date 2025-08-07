import os
import shutil
from glob import glob
import yaml

# === Paths ===
roboflow_images_dir = "/home/nvidia07/cat-breed-detector/data/cat_breeds_roboflow/test/images"
roboflow_labels_dir = "/home/nvidia07/cat-breed-detector/data/cat_breeds_roboflow/test/labels"
dataset_root = "/home/nvidia07/cat-breed-detector/data"
images_base = os.path.join(dataset_root, "images")
labels_base = os.path.join(dataset_root, "labels")
yaml_path = "/home/nvidia07/cat-breed-detector/data/cat_breeds_roboflow/data.yaml"

# === Breed name overrides ===
short_name_map = {
    "British Shorthair": "British",
    "Maine Coon": "Maine",
    "Egyptian Mau": "Egyptian"
}

# === Load breed names from YAML ===
with open(yaml_path, 'r') as f:
    data_yaml = yaml.safe_load(f)
breed_names = data_yaml['names']

# === Build name-to-folder map ===
def get_folder_name(breed):
    return short_name_map.get(breed, breed.replace(" ", " "))  # preserve spaces

# === Counters for renaming ===
rename_counters = {}

# === Ensure breed subfolders exist ===
def ensure_subfolders(breed_folder):
    for base in [images_base, labels_base]:
        for split in ['train', 'val']:
            os.makedirs(os.path.join(base, split, breed_folder), exist_ok=True)

# === Sorting logic ===
image_files = sorted(glob(os.path.join(roboflow_images_dir, "*.jpg")))

for image_path in image_files:
    filename = os.path.basename(image_path)
    base_name = os.path.splitext(filename)[0]
    label_path = os.path.join(roboflow_labels_dir, base_name + ".txt")

    if not os.path.exists(label_path):
        print(f"[!] Skipping {filename}, no label found.")
        continue

    with open(label_path, 'r') as f:
        first_line = f.readline().strip()

    if not first_line:
        print(f"[!] Skipping {filename}, label is empty.")
        continue

    try:
        class_id = int(first_line.split()[0])
        breed = breed_names[class_id]
        folder_name = get_folder_name(breed)
    except (IndexError, ValueError) as e:
        print(f"[!] Skipping {filename}, invalid label format: {e}")
        continue

    ensure_subfolders(folder_name)
    count = rename_counters.get(folder_name, 1)

    # New names
    new_img_name = f"{folder_name.replace(' ', '_')}_{count}.jpg"
    new_lbl_name = f"{folder_name.replace(' ', '_')}_{count}.txt"

    # Alternate between train and val
    split = "train" if count % 5 != 0 else "val"

    # Target paths
    target_img = os.path.join(images_base, split, folder_name, new_img_name)
    target_lbl = os.path.join(labels_base, split, folder_name, new_lbl_name)

    # Copy files
    shutil.copy(image_path, target_img)
    shutil.copy(label_path, target_lbl)

    rename_counters[folder_name] = count + 1

print("\n✅ Sorting complete.")