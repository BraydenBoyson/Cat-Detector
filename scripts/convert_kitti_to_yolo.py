import os

# Paths
labels_kitti_dir = "data/kitti_labels"
images_dir = "data/images"
yolo_labels_dir = "data/labels"
splits = ["train", "val"]

# Class mapping (only 'cat')
class_map = {"cat": 0}

# Create output folders
for split in splits:
    os.makedirs(f"data/images/{split}", exist_ok=True)
    os.makedirs(f"data/labels/{split}", exist_ok=True)

# Convert KITTI format to YOLO format
def kitti_to_yolo(txt_file, out_file, img_width, img_height):
    with open(txt_file, "r") as f:
        lines = f.readlines()

    yolo_lines = []
    for line in lines:
        parts = line.strip().split()
        cls_name = parts[0].lower()
        if cls_name != "cat":
            continue
        x1, y1, x2, y2 = map(float, parts[4:8])
        xc = (x1 + x2) / 2 / img_width
        yc = (y1 + y2) / 2 / img_height
        w = (x2 - x1) / img_width
        h = (y2 - y1) / img_height
        yolo_lines.append(f"{class_map['cat']} {xc} {yc} {w} {h}")

    with open(out_file, "w") as f:
        f.write("\n".join(yolo_lines))


for split in splits:
    with open(f"data/{split}.txt") as f:
        files = f.read().splitlines()
    for filename in files:
        img_path = os.path.join(images_dir, filename)
        label_path = os.path.join(labels_kitti_dir, filename.replace(".jpg", ".txt"))
        if not os.path.exists(label_path):
            continue
        # Get image size
        from PIL import Image
        with Image.open(img_path) as im:
            w, h = im.size
        # Convert label
        out_txt = f"data/labels/{split}/{filename.replace('.jpg', '.txt')}"
        kitti_to_yolo(label_path, out_txt, w, h)
        # Copy image
        os.system(f"cp '{img_path}' 'data/images/{split}/'")
