from ultralytics import YOLO
import cv2
import numpy as np


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



def crop_entity(image, coordinates, save_path):
    coords = np.array(coordinates)
    i = cv2.imread(image)
    xmin = int(coords[0])
    ymin = int(coords[1])
    xmax = int(coords[2])
    ymax = int(coords[3])
    # Crop image
    cropped_image = i[ymin:ymax, xmin:xmax]

    # Save cropped image
    cv2.imwrite(save_path, cropped_image)



def get_names():
    model = load_pretrained_model()
    res = model(source="https://ultralytics.com/images/bus.jpg")
    return (res[0].names)


model = YOLO(
    "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8m.pt")
results = model.predict("Aithon/All_Images/Mist.jpeg")
result = results[0]
boxes = result.boxes
names = get_names()
count = 0
for box in boxes:
    cords = box.xyxy[0]
    class_id = box.cls[0].item()
    conf = box.conf[0].item()
    image = "Aithon/All_Images/Mist.jpeg"
    save_path = "Aithon/problem5_output/1/1"+str(count)+".jpg"

    count += 1
    # # GET CLASS IDS for problems 2-5
    # print("Object type:", names[int(class_id)].title())

    # # Get Coordinates for problem 4-5
    # print("Coordinates:", cords)

    # # Get Probabilities for none
    # print("Probability:", conf)
