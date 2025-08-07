import os
import yaml

# === Paths ===
project_root = "/home/nvidia07/cat-breed-detector"
roboflow_yaml_path = os.path.join(project_root, "data/cat_breeds_roboflow/data.yaml")

images_train = os.path.join(project_root, "data/images/train")
images_val = os.path.join(project_root, "data/images/val")
labels_train = os.path.join(project_root, "data/labels/train")
labels_val = os.path.join(project_root, "data/labels/val")

# === Load Roboflow breed names ===
with open(roboflow_yaml_path, "r") as f:
    data_yaml = yaml.safe_load(f)

roboflow_breeds = data_yaml["names"]

# === Mapping short forms
breed_rename_map = {
    "British Shorthair": "British",
    "Maine Coon": "Maine",
    "Egyptian Mau": "Egyptian"
}

# === Existing folders
existing_breeds = set(os.listdir(images_train))

# === Dry Run: Show which folders would be created
print("\n📋 DRY RUN: These folders WOULD be created:\n")
for breed in roboflow_breeds:
    normalized_breed = breed_rename_map.get(breed, breed)

    if normalized_breed in existing_breeds:
        print(f"✅ Skipping existing breed: {normalized_breed}")
        continue

    for base in [images_train, images_val, labels_train, labels_val]:
        breed_path = os.path.join(base, normalized_breed)
        print(f"📁 Would create: {breed_path}")