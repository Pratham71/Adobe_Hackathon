from PIL import Image
import os
from ultralytics import YOLO


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


def list_files(directory, external=""):
    # list to store files
    res = []

    # Iterate directory
    for file_path in os.listdir(directory):
        # add filename to list
        res.append(external+file_path)
    return res


def create_directory(entity):
    path = entity
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def main():

    model = load_pretrained_model()

    # Classifing Directory
    directory = "Aithon/All_Images/"

    # Getting list of flies
    image_list = list_files(directory)

    # Iterating over list
    for img in image_list:
        # Predicting for each image
        res = model.predict(str(directory+img))[0]

        res = res.plot(line_width=1)
        res = res[:, :, ::-1]

        # Making boxes
        res = Image.fromarray(res)

        # Making/Checking output directory
        output_path = "Aithon/problem1_output/"
        create_directory(output_path)

        # Saving file in destination
        destination = output_path+img
        res.save(destination)


if __name__ == "__main__":
    # Baseline 24.176857 seconds
    main()
