import os
import shutil
from pathlib import Path

# --- CONFIG ---
undo_base = Path("undo_roboflow")
image_base = Path("data/images/train")
label_base = Path("data/labels/train")

# --- Function to move files ---
def move_files(split_type):
    img_src = undo_base / "images" / split_type
    lbl_src = undo_base / "labels" / split_type

    if not img_src.exists():
        print(f"[!] Source image folder not found: {img_src}")
        return

    for file in img_src.glob("*.jpg"):
        # Extract breed from filename (before the first underscore)
        breed = file.stem.split("_")[0]

        img_dest_dir = image_base / breed
        lbl_dest_dir = label_base / breed

        img_dest_dir.mkdir(parents=True, exist_ok=True)
        lbl_dest_dir.mkdir(parents=True, exist_ok=True)

        shutil.move(str(file), str(img_dest_dir / file.name))

        # Move matching label file
        label_file = lbl_src / f"{file.stem}.txt"
        if label_file.exists():
            shutil.move(str(label_file), str(lbl_dest_dir / label_file.name))
        else:
            print(f"[!] No label found for: {file.name}")

    print(f"[✓] Finished moving {split_type} data.")

# Run for 'train'
move_files("train")