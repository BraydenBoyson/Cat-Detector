import os
import shutil

DATA_DIR = "/home/nvidia07/cat-breed-detector/data"

def merge_val_to_train(data_type):
    val_root = os.path.join(DATA_DIR, data_type, "val")
    train_root = os.path.join(DATA_DIR, data_type, "train")

    for breed_name in os.listdir(val_root):
        val_breed_dir = os.path.join(val_root, breed_name)
        train_breed_dir = os.path.join(train_root, breed_name)

        if not os.path.isdir(val_breed_dir):
            continue  # Skip if it's not a folder

        os.makedirs(train_breed_dir, exist_ok=True)

        for file_name in os.listdir(val_breed_dir):
            src = os.path.join(val_breed_dir, file_name)
            dst = os.path.join(train_breed_dir, file_name)

            if not os.path.exists(dst):  # Avoid overwriting
                shutil.copy2(src, dst)
                print(f"Copied {src} -> {dst}")
            else:
                print(f"Skipped (already exists): {dst}")

def main():
    merge_val_to_train("images")
    merge_val_to_train("labels")

if __name__ == "__main__":
    main()