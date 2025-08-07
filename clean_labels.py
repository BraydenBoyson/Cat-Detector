import os

def is_label_valid(path):
    with open(path, "r") as f:
        lines = f.readlines()
        if not lines:
            return False
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                return False
            class_id, *coords = parts
            if not class_id.isdigit() or int(class_id) < 0:
                return False
            for c in coords:
                try:
                    val = float(c)
                    if val < 0 or val > 1:
                        return False
                except ValueError:
                    return False
    return True

def main():
    base_dirs = ["data/labels/train", "data/labels/val"]
    removed = 0
    for base in base_dirs:
        print(f"Checking {base} ...")
        for filename in os.listdir(base):
            if filename.endswith(".txt"):
                path = os.path.join(base, filename)
                if not is_label_valid(path):
                    os.remove(path)
                    removed += 1
                    print(f"Removed invalid label file: {filename}")
    print(f"\nRemoved {removed} invalid label files.")

if __name__ == "__main__":
    main()