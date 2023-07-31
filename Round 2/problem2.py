from ultralytics import YOLO
import csv
import shutil
from common_functions import list_files, load_pretrained_model, get_names, read_file


def entity_counter(info, names):
    entity_count = {"Entity": "Count"}
    for line in info:
        i = int(line.split()[0])
        if names[i].title() in list(entity_count.keys()):
            entity_count[names[i].title()] += 1
        else:
            entity_count[names[i].title()] = 1
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
    directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/All_Images/"

    names = get_names()

    # Getting list of flies
    image_list = list_files(directory)
    # Iterating over list
    for img in image_list:

        # Predicting for each image
        res = model(directory+img, save_txt=True)

        # Reading file
        info = read_file(img, res[0])

        # Dictionary count
        entity_count = entity_counter(info, names)

        # Opening/Creating file for writing
        csv_filepath = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem2_output/" + \
            img.split(".")[0]+".csv"
        write_in_csv(entity_count, csv_filepath)

    runs_directory = "C:/Users/allof/Downloads/Timepass/runs"
    shutil.rmtree(runs_directory)


if __name__ == '__main__':
    main()
