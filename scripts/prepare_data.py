import os
import tarfile
import urllib.request
import shutil
from xml.etree import ElementTree
from sklearn.model_selection import train_test_split # type: ignore

# Directories
BASE_DIR = os.path.expanduser('~/cat-breed-detector/data')
IMAGES_TAR = "images.tar.gz"
ANNOTATIONS_TAR = "annotations.tar.gz"
IMAGE_URL = "https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz"
ANNOTATION_URL = "https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz"

# Cat breeds from the dataset
CAT_BREEDS = {
    "abyssinian", "bengal", "birman", "bombay",
    "british_shorthair", "egyptian_mau", "maine_coon",
    "persian", "ragdoll", "russian_blue", "siamese", "sphynx"
}

def download_and_extract():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.chdir(BASE_DIR)

    print("Downloading images...")
    urllib.request.urlretrieve(IMAGE_URL, IMAGES_TAR)
    print("Downloading annotations...")
    urllib.request.urlretrieve(ANNOTATION_URL, ANNOTATIONS_TAR)

    print("Extracting images...")
    with tarfile.open(IMAGES_TAR) as tar:
        tar.extractall(path=os.path.join(BASE_DIR, 'images_raw'))

    print("Extracting annotations...")
    with tarfile.open(ANNOTATIONS_TAR) as tar:
        tar.extractall(path=os.path.join(BASE_DIR, 'annotations_raw'))

    os.remove(IMAGES_TAR)
    os.remove(ANNOTATIONS_TAR)

def filter_cat_images():
    images_raw = os.path.join(BASE_DIR, 'images_raw')
    annotations_raw = os.path.join(BASE_DIR, 'annotations_raw', 'xmls')
    image_dir = os.path.join(BASE_DIR, 'images')
    annot_dir = os.path.join(BASE_DIR, 'annotations')

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(annot_dir, exist_ok=True)

    count = 0
    for filename in os.listdir(images_raw):
        if not filename.endswith('.jpg'):
            continue

        breed = filename.split('_')[0].lower()
        if breed in CAT_BREEDS:
            img_src = os.path.join(images_raw, filename)
            xml_name = filename.replace('.jpg', '.xml')
            xml_src = os.path.join(annotations_raw, xml_name)

            if os.path.exists(xml_src):
                shutil.copy(img_src, os.path.join(image_dir, filename))
                shutil.copy(xml_src, os.path.join(annot_dir, xml_name))
                count += 1

    print(f"✔️ Filtered and copied {count} cat images with annotations.")

def split_train_val():
    image_dir = os.path.join(BASE_DIR, 'images')
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

    train, val = train_test_split(image_files, test_size=0.2, random_state=42)

    train_txt = os.path.join(BASE_DIR, 'train', 'train.txt')
    val_txt = os.path.join(BASE_DIR, 'val', 'val.txt')
    os.makedirs(os.path.dirname(train_txt), exist_ok=True)
    os.makedirs(os.path.dirname(val_txt), exist_ok=True)

    with open(train_txt, 'w') as f:
        for item in train:
            f.write(os.path.abspath(os.path.join(image_dir, item)) + '\n')

    with open(val_txt, 'w') as f:
        for item in val:
            f.write(os.path.abspath(os.path.join(image_dir, item)) + '\n')

    print(f"✔️ Created train/val split: {len(train)} train, {len(val)} val.")

if __name__ == '__main__':
    download_and_extract()
    filter_cat_images()
    split_train_val()