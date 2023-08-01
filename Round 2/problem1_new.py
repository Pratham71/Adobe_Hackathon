from ultralytics import YOLO
from common_functions import get_names
model = YOLO(
    "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8m.pt")
results = model.predict("https://ultralytics.com/images/bus.jpg")
result = results[0]
boxes = result.boxes
names = get_names()
for box in boxes:
    cords = box.xyxy[0].tolist()
    class_id = box.cls[0].item()
    conf = box.conf[0].item()
    print("Object type:", names[int(class_id)].title())
    print("Coordinates:", cords)
    print("Probability:", conf)
