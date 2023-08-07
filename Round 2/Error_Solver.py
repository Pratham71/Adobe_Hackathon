from ultralytics import YOLO
from PIL import Image
import torch
import torchvision
import torchvision.transforms as T


def load_pretrained_model():
    # loading pretrained models
    model = YOLO(
        "models/yolov8n.pt")
    model = YOLO(
        "models/yolov8m.pt")
    model = YOLO(
        "models/yolov8l.pt")
    model = YOLO(
        "models/yolov8s.pt")
    return model


def get_names():
    model = load_pretrained_model()
    res = model(source="https://ultralytics.com/images/bus.jpg")
    return (res[0].names)


model = YOLO(
    "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8m.pt")
results = model.predict("Aithon/All_Images/1.jpg")
result = results[0]
boxes = result.boxes
names = get_names()
count = 0
transform = T.ToPILImage()
for box in boxes:
    cords = transform(box.xyxy[0])
    class_id = box.cls[0].item()
    conf = box.conf[0].item()
    im = Image.open("Aithon/All_Images/1.jpg")
    cropped = im.crop(cords)
    cropped.save("Aithon/problem5_output/1/1"+str(count)+".jpg")
    count += 1
    # # GET CLASS IDS for problems 2-5
    # print("Object type:", names[int(class_id)].title())

    # # Get Coordinates for problem 4-5
    # print("Coordinates:", cords)

    # # Get Probabilities for none
    # print("Probability:", conf)
