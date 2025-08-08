# C.A.T. (Cat Acknowledgement Technology)

The project which I have created is a tool that is supposed to be used to detect cats and then classify the breed of the cat being detected

## Installation

Install yolov8

```bash
  pip install ultralytics
```
Train AI Models
```bash
yolo task=classify mode=train model=yolov8n-cls.pt data=/home/nvidia07/cat-breed-detector/data/images epochs=20 imgsz=128
```
Place images you want to test into 
```bash
/home/nvidia07/cat-breed-detector/data/test
```
To run the prediction
```bash
yolo task=classify mode=predict model=/home/nvidia07/cat-breed-detector/runs/classify/train/weights/best.pt source=/home/nvidia07/cat-breed-detector/data/test
```
