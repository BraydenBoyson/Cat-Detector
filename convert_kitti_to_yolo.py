import os
from PIL import Image

# Constants
CLASS_MAP = {"cat": 0}
KITTI_DIR = "data/kitti_labels"
IMAGE_DIRS = {"train": "data/images/train", "val": "data/images/val"}
LABEL_DIRS = {"train": "data/labels/train", "val": "data/labels/val"}

# Ensure label dirs exist
for path in LABEL_DIRS.values():
    os.makedirs(path, exist_ok=True)

def convert_kitti_line_to_yolo(line, img_w, img_h):
    parts = line.strip().split()
    if len(parts) < 5:
        return None
    class_name = parts[0].lower()
    if class_name != "cat":
        return None
    try:
        xmin, ymin, xmax, ymax = map(float, parts[4:8])
        x_center = ((xmin + xmax) / 2) / img_w
        y_center = ((ymin + ymax) / 2) / img_h
        width = (xmax - xmin) / img_w
        height = (ymax - ymin) / img_h
        return f"{CLASS_MAP['cat']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
    except Exception:
        return None

def process_split(split):
    image_dir = IMAGE_DIRS[split]
    label_dir = LABEL_DIRS[split]

    image_files = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]

    count = 0
    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        kitti_path = os.path.join(KITTI_DIR, f"{base_name}.txt")
        yolo_path = os.path.join(label_dir, f"{base_name}.txt")
        image_path = os.path.join(image_dir, image_file)

        if not os.path.exists(kitti_path):
            continue

        try:
            with Image.open(image_path) as img:
                w, h = img.size
        except Exception:
            continue

        with open(kitti_path, "r") as f:
            lines = f.readlines()

        yolo_lines = []
        for line in lines:
            yolo_line = convert_kitti_line_to_yolo(line, w, h)
            if yolo_line:
                yolo_lines.append(yolo_line)

        if yolo_lines:
            with open(yolo_path, "w") as out_f:
                out_f.write("\n".join(yolo_lines) + "\n")
            count += 1

    print(f"✅ {count} YOLO labels created for {split} set.")

if __name__ == "__main__":
    process_split("train")
    process_split("val")