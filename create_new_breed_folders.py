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

# === Mapping long names to short folder names used in your dataset
breed_rename_map = {
    "British Shorthair": "British",
    "Maine Coon": "Maine",
    "Egyptian Mau": "Egyptian"
}

# === Get current breed folders
existing_breeds = set(os.listdir(images_train))

# === Create folders for new breeds only
print("\n📁 Creating new breed folders if missing:\n")
for breed in roboflow_breeds:
    normalized_breed = breed_rename_map.get(breed, breed)

    if normalized_breed in existing_breeds:
        print(f"✅ Already exists: {normalized_breed}")
        continue

    for base in [images_train, images_val, labels_train, labels_val]:
        breed_path = os.path.join(base, normalized_breed)
        os.makedirs(breed_path, exist_ok=True)
        print(f"📁 Created: {breed_path}")