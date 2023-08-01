import os
from ultralytics import YOLO
import shutil

# List Of Commmon Functions


def list_files(directory):
    # list to store files
    res = []

    # Iterate directory
    for file_path in os.listdir(directory):
        # add filename to list
        res.append(file_path)
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


def read_file(img, result):
    filepath = "C:/Users/allof/Downloads/Timepass/" + \
        result.save_dir.replace("\\", "/")+"/labels/" + \
        img.split(".")[0]+".txt"
    with open(filepath) as file:
        info = file.readlines()
    return info


def list_of_entities(info, names):
    entities = []
    for line in info:
        i = int(line.split()[0])
        if names[i].title() not in entities:
            entities.append(names[i].title())
    return entities


def create_directory(entity):
    path = entity
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def delete_runs():
    runs_directory = "C:/Users/allof/Downloads/Timepass/runs"
    shutil.rmtree(runs_directory)
