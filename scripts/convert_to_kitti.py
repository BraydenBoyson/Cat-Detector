import os
import xml.etree.ElementTree as ET

# Base paths
BASE_DIR = os.path.expanduser('~/cat-breed-detector/data')
ANNOT_DIR = os.path.join(BASE_DIR, 'annotations')
KITTI_DIR = os.path.join(BASE_DIR, 'kitti_labels')
os.makedirs(KITTI_DIR, exist_ok=True)

# Cat breeds list (all lowercase, underscores instead of spaces)
CAT_BREEDS = ["cat"]

def convert_xml_to_kitti(xml_file, output_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        objects = root.findall('object')

        if not objects:
            print(f"⚠️ No objects found in {xml_file}")
            return

        wrote_any = False
        with open(output_file, 'w') as out:
            for obj in objects:
                name = obj.find('name').text
                if not name:
                    continue

                # Normalize breed name: lowercase, replace spaces with underscores
                name_norm = name.lower().replace(" ", "_")

                # Only process if it's a cat breed
                if name_norm not in CAT_BREEDS:
                    continue

                bbox = obj.find('bndbox')
                if bbox is None:
                    continue

                xmin = int(float(bbox.find('xmin').text))
                ymin = int(float(bbox.find('ymin').text))
                xmax = int(float(bbox.find('xmax').text))
                ymax = int(float(bbox.find('ymax').text))

                # Write KITTI format
                line = f"{name_norm} 0 0 0 {xmin} {ymin} {xmax} {ymax} 0 0 0 0 0 0 0\n"
                out.write(line)
                wrote_any = True

        # Remove the output file if nothing was written
        if not wrote_any:
            os.remove(output_file)

    except Exception as e:
        print(f"❌ Error processing {xml_file}: {e}")

def convert_all():
    print("🔄 Converting XML annotations to KITTI format (cats only)...")
    for xml_file in os.listdir(ANNOT_DIR):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(ANNOT_DIR, xml_file)
            output_path = os.path.join(KITTI_DIR, xml_file.replace('.xml', '.txt'))
            convert_xml_to_kitti(xml_path, output_path)

    print(f"✅ Finished conversion. Check the folder: {KITTI_DIR}")

if __name__ == '__main__':
    convert_all()