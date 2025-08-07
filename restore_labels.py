import os
from pathlib import Path

# Path to your dataset
project_dir = Path("/home/nvidia07/cat-breed-detector")
image_dir = project_dir / "data/images"
label_dir = project_dir / "data/labels"

# This must match the order in your cat_dataset.yaml
breed_names = [
    "Abyssinian", "American Curl", "American Short Hair", "Balinese", "Bengal",
    "Birman", "Bombay", "British", "Burmese", "Calico", "Chartreux", "Cornish Rex",
    "Devon Rex", "Dilute Tortoiseshell", "Domestic Long Hair", "Domestic Medium Hair",
    "Domestic Short Hair", "Egyptian", "Havana", "Himalayan", "Japanese Bobtail",
    "Korat", "Maine", "Manx", "Munchkin", "Norwegian Forest Cat", "Ocicat",
    "Oriental Short Hair", "Oriental Tabby", "Persian", "Pixiebob", "Ragamuffin",
    "Ragdoll", "Russian Blue", "Scottish Fold", "Selkirk Rex", "Siamese", "Siberian",
    "Silver", "Snowshoe", "Sphynx", "Tabby", "Turkish Angora", "Turkish Van"
]

# Map breed name to class index
breed_to_index = {name: idx for idx, name in enumerate(breed_names)}

# For both 'train' and 'val'
for split in ["train", "val"]:
    img_split_dir = image_dir / split
    lbl_split_dir = label_dir / split

    for breed_name in breed_names:
        img_breed_dir = img_split_dir / breed_name
        lbl_breed_dir = lbl_split_dir / breed_name
        lbl_breed_dir.mkdir(parents=True, exist_ok=True)

        if not img_breed_dir.exists():
            continue

        for img_file in img_breed_dir.glob("*.jpg"):
            label_file = lbl_breed_dir / f"{img_file.stem}.txt"
            with open(label_file, "w") as f:
                f.write(f"{breed_to_index[breed_name]}\n")

print("✅ Label restoration complete.")