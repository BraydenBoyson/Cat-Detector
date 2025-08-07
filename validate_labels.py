import os

def validate_label_file(path):
    errors = []
    with open(path, "r") as f:
        lines = f.readlines()
        if not lines:
            errors.append("Empty file")
        for i, line in enumerate(lines, 1):
            parts = line.strip().split()
            if len(parts) != 5:
                errors.append(f"Line {i}: Expected 5 values, got {len(parts)}")
                continue
            class_id, *coords = parts
            # Check class_id is integer and >= 0
            if not class_id.isdigit() or int(class_id) < 0:
                errors.append(f"Line {i}: Invalid class id '{class_id}'")
            # Check coords are floats between 0 and 1
            for c in coords:
                try:
                    val = float(c)
                    if val < 0 or val > 1:
                        errors.append(f"Line {i}: Coordinate {val} out of range [0,1]")
                except ValueError:
                    errors.append(f"Line {i}: Coordinate '{c}' is not a float")
    return errors

def main():
    base_dirs = ["data/labels/train", "data/labels/val"]
    total_files = 0
    bad_files = 0
    for base in base_dirs:
        print(f"Checking label files in {base} ...")
        for filename in os.listdir(base):
            if filename.endswith(".txt"):
                total_files += 1
                path = os.path.join(base, filename)
                errors = validate_label_file(path)
                if errors:
                    bad_files += 1
                    print(f"\nErrors in {filename}:")
                    for err in errors:
                        print(f"  - {err}")
    print(f"\nChecked {total_files} label files, found errors in {bad_files} files.")

if __name__ == "__main__":
    main()