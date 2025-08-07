from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO('/home/nvidia07/cat-breed-detector/runs/detect/train7/weights/best.pt')

# Path to your test image
image_path = '/home/nvidia07/cat-breed-detector/test_images/abyssinian.jpg'

# Run detection
results = model.predict(source=image_path, save=True, imgsz=640, conf=0.25)

print("✅ Detection complete. Check the 'runs/detect/predict' folder for the output image.")
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO('/home/nvidia07/cat-breed-detector/runs/detect/train7/weights/best.pt')

# Path to your test image
image_path = '/home/nvidia07/cat-breed-detector/test_images/abyssinian.jpg'

# Run detection
results = model.predict(source=image_path, save=True, imgsz=640, conf=0.25)

print("✅ Detection complete. Check the 'runs/detect/predict' folder for the output image.")

