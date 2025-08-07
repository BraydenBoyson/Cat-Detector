import os
import shutil

# Config
project_root = os.path.abspath(".")
data_root = os.path.join(project_root, "data")
image_root = os.path.join(data_root, "images")
train_src = os.path.join(data_root, "train")
val_src = os.path.join(data_root, "val")
train_dst = os.path.join(image_root, "train")
val_dst = os.path.join(image_root, "val")
yaml_path = os.path.join(project_root, "cat_breeds_dataset.yaml")

# Create destination dirs
os.makedirs(train_dst, exist_ok=True)
os.makedirs(val_dst, exist_ok=True)

# Move training folders
for breed_dir in os.listdir(train_src):
    src_path = os.path.join(train_src, breed_dir)
    dst_path = os.path.join(train_dst, breed_dir)
    if os.path.isdir(src_path):
        shutil.move(src_path, dst_path)

# Move val folders if any
if os.path.exists(val_src):
    for breed_dir in os.listdir(val_src):
        src_path = os.path.join(val_src, breed_dir)
        dst_path = os.path.join(val_dst, breed_dir)
        if os.path.isdir(src_path):
            shutil.move(src_path, dst_path)

# List breed names
breed_names = sorted(os.listdir(train_dst))

# Create dataset.yaml
with open(yaml_path, "w") as f:
    f.write(f"path: {image_root}\n")
    f.write("train: train\n")
    f.write("val: val\n")
    f.write(f"nc: {len(breed_names)}\n")
    f.write("names:\n")
    for name in breed_names:
        f.write(f"  - {name}\n")

print(f"✅ Done. Dataset ready at {image_root}")
print(f"📄 YAML saved to: {yaml_path}")