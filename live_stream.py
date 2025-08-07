from flask import Flask, Response
import cv2
from ultralytics import YOLO
import threading

app = Flask(__name__)

model = YOLO('/home/nvidia07/cat-breed-detector/runs/classify/train/weights/best.pt')
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run model prediction
        results = model.predict(frame, imgsz=224)
        pred = results[0]
        # Get top predicted class and confidence
        if len(pred.probs) > 0:
            top_idx = int(pred.probs.top1)
            label = pred.names[top_idx]
            confidence = pred.probs.data[top_idx].item()
            text = f"{label} ({confidence:.2f})"
            # Annotate frame
            cv2.putText(frame, text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield frame in multipart format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
        <head><title>Cat Breed Classifier Live Stream</title></head>
        <body>
            <h1>Live Stream with Classification</h1>
            <img src="/video_feed" width="640" height="480"/>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)