from ultralytics import YOLO
import os
import shutil
from common_functions import list_files, load_pretrained_model, get_names, read_file, list_of_entities, create_directory, delete_runs


def copy_img(src_file, dst_file):
    shutil.copy(src_file, dst_file)


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

    delete_runs()


if __name__ == '__main__':
    main()
