import os
import shutil

# Paths
undo_dir = "/home/nvidia07/cat-breed-detector/undo_roboflow"
images_train_dir = "/home/nvidia07/cat-breed-detector/data/images/train"
labels_train_dir = "/home/nvidia07/cat-breed-detector/data/labels/train"

# Breed names by class ID from data.yaml
breed_names = [
    'Abyssianian', 'American Curl', 'American Short Hair', 'American Wirehair', 'Balinese',
    'Bengal', 'Birman', 'Bombay', 'British Shorthair', 'Burmese', 'Burmilla', 'Calico',
    'Canadian Hairless', 'Chartreux', 'Cornish Rex', 'Cymric', 'Devon Rex', 'Dilute Tortoiseshell',
    'Domestic Long Hair', 'Domestic Medium Hair', 'Domestic Short Hair', 'Egyptian Mau',
    'Exotic Shorthair', 'Extra-Toe', 'Havana', 'Himalayan', 'Japanese Bobtail', 'Javanese',
    'Korat', 'Laperm', 'Maine Coon', 'Manx', 'Munchkin', 'Norwegian Forest Cat', 'Ocicat',
    'Oriental Long Hair', 'Oriental Short Hair', 'Oriental Tabby', 'Persian', 'Pixiebob',
    'Ragamuffin', 'Ragdoll', 'Russian Blue', 'Scottish Fold', 'Selkirk Rex', 'Siamese',
    'Siberian', 'Silver', 'Singapura', 'Snowshoe', 'Somali', 'Sphynx', 'Tabby',
    'Turkish Angora', 'Turkish Van'
]

# Normalize known short breed subfolder names
short_breed_map = {
    "British Shorthair": "British",
    "Maine Coon": "Maine",
    "Egyptian Mau": "Egyptian"
}

# Breed counters for unique filenames
breed_file_counters = {}

def get_breed_name(class_id):
    try:
        name = breed_names[int(class_id)]
        return short_breed_map.get(name, name)
    except (IndexError, ValueError):
        return None

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Prepare breed folders and counters
for name in breed_names:
    name = short_breed_map.get(name, name)
    ensure_dir(os.path.join(images_train_dir, name))
    ensure_dir(os.path.join(labels_train_dir, name))
    breed_file_counters[name] = len(os.listdir(os.path.join(images_train_dir, name)))

# Process all files in undo_roboflow
for file_name in os.listdir(undo_dir):
    if not file_name.endswith(".jpg"):
        continue

    image_path = os.path.join(undo_dir, file_name)
    label_path = os.path.join(undo_dir, os.path.splitext(file_name)[0] + ".txt")

    if not os.path.exists(label_path):
        continue

    with open(label_path, "r") as f:
        first_line = f.readline().strip()
        if not first_line:
            continue
        class_id = first_line.split()[0]
        breed_name = get_breed_name(class_id)
        if not breed_name:
            continue

    # Generate unique name
    breed_file_counters[breed_name] += 1
    count = breed_file_counters[breed_name]
    safe_breed = breed_name.replace(" ", "_")

    new_image_name = f"{safe_breed}_{count}.jpg"
    new_label_name = f"{safe_breed}_{count}.txt"

    dst_img = os.path.join(images_train_dir, breed_name, new_image_name)
    dst_lbl = os.path.join(labels_train_dir, breed_name, new_label_name)

    shutil.copy(image_path, dst_img)
    shutil.copy(label_path, dst_lbl)

print("[✔] All undo_roboflow images and labels have been sorted and renamed.")