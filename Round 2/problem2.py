import os
from ultralytics import YOLO
import csv


def list_files(directory, external=""):
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


def entity_counter(info, names):
    # Initialising Dictionary
    entity_count = {"Entity": "Count"}

    # Counting info
    for line in info:
        if names[line].title() in list(entity_count.keys()):
            entity_count[names[line].title()] += 1
        else:
            entity_count[names[line].title()] = 1

    # Couting and appending Total
    entity_count['Total'] = sum(list(entity_count.values())[1:])
    return entity_count


def write_in_csv(entity_count, csv_filepath):

    with open(csv_filepath, "w", newline="") as file:
        count = 0
        keys = list(entity_count.keys())
        values = list(entity_count.values())
        writer = csv.writer(file)

        # Writing in File
        while count < len(entity_count):
            writer.writerow([keys[count], values[count]])
            count += 1


def main():

    model = load_pretrained_model()

    # Classifing Directory
    directory = "Aithon/All_Images/"

    names = get_names()

    # Getting list of flies
    image_list = list_files(directory)

    # Iterating over list
    for img in image_list:

        # Predicting for each image
        res = model(directory+img)

        # Get List of class ids
        info = get_info_using_res(res[0])

        # Dictionary count
        entity_count = entity_counter(info, names)

        # Making/Checking ouptput directory
        output_path = "Aithon/problem2_output/"
        create_directory(output_path)

        # Opening/Creating file for writing
        csv_filepath = output_path + img.split(".")[0]+".csv"
        write_in_csv(entity_count, csv_filepath)


if __name__ == '__main__':
    # Baseline 21.603803 seconds
    main()
