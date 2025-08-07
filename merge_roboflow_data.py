import os
import shutil

# Define project path and dataset paths
project_root = "/home/nvidia07/cat-breed-detector"
roboflow_path = os.path.join(project_root, "data", "cat_breeds_roboflow")
target_images = os.path.join(project_root, "data", "images")
target_labels = os.path.join(project_root, "data", "labels")

# Mapping of Roboflow split to your structure
splits = {
    "train": "train",
    "valid": "val"
}

# Extract breed name from file (e.g., Bengal_123.jpg -> Bengal)
def extract_breed(filename):
    return filename.split("_")[0]

# Loop through roboflow splits and organize into your structure
for roboflow_split, target_split in splits.items():
    for dtype in ["images", "labels"]:
        source_dir = os.path.join(roboflow_path, roboflow_split, dtype)
        target_base = target_images if dtype == "images" else target_labels
        target_dir = os.path.join(target_base, target_split)

        if not os.path.exists(source_dir):
            continue

        for file in os.listdir(source_dir):
            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.txt')):
                continue

            breed = extract_breed(file)
            breed_folder = os.path.join(target_dir, breed)
            os.makedirs(breed_folder, exist_ok=True)

            src = os.path.join(source_dir, file)
            dst = os.path.join(breed_folder, file)

            if not os.path.exists(dst):  # Avoid overwriting
                shutil.move(src, dst)
                print(f"Moved: {file} -> {breed_folder}")
            else:
                print(f"Skipped (already exists): {file}")