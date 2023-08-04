import os
from ultralytics import YOLO

# List Of Commmon Functions


def list_files(directory,external = ""):
    # list to store files
    res = []

    # Iterate directory
    for file_path in os.listdir(directory):
        # add filename to list
        res.append(external+file_path)
    return res


def load_pretrained_model():
    # load a pretrained model
    model = YOLO(
        "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8n.pt")
    model = YOLO(
        "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8m.pt")
    model = YOLO(
        "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8l.pt")
    model = YOLO(
        "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/models/yolov8s.pt")
    return model


def get_names():
    model = load_pretrained_model()
    res = model(source="https://ultralytics.com/images/bus.jpg")
    return (res[0].names)


def list_of_entities(info, names):
    entities = []
    for i in info:
        if names[i].title() not in entities:
            entities.append(names[i].title())
    return entities


def create_directory(entity):
    path = entity
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def get_info_using_res(res):
    info = []
    boxes = res.boxes
    for box in boxes:
        info.append(int(box.cls[0].item()))
    return info
