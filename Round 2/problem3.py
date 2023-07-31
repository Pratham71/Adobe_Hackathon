from ultralytics import YOLO
import os
import shutil
from common_functions import list_files, load_pretrained_model, get_names, read_file


def copy_img(src_file, dst_file):
    shutil.copy(src_file, dst_file)


def create_directory(entity):
    path = entity
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def list_of_entities(info, names):
    entities = []
    for line in info:
        i = int(line.split()[0])
        if names[i].title() not in entities:
            entities.append(names[i].title())
    return entities


def main():
    model = load_pretrained_model()

    names = get_names()

    dest_path = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem3_output/"

    # Classifing Directory
    directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/All_Images/"

    # Getting list of flies
    image_list = list_files(directory)
    # Iterating over list
    for img in image_list:

        # Predicting for each image
        res = model(directory+img, save_txt=True)

        # Reading file
        info = read_file(img, res[0])

        # Making List of Entities in Image
        entities = list_of_entities(info, names)

        for entity in entities:
            create_directory(dest_path+entity)
            copy_img(directory+img, dest_path+entity)

    runs_directory = "C:/Users/allof/Downloads/Timepass/runs"
    shutil.rmtree(runs_directory)


if __name__ == '__main__':
    main()
