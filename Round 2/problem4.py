import csv
import os
from ultralytics import YOLO


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


def create_directory(entity):
    path = entity
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def checkCount(entity, list_of_names):
    # Counting the last value and adding 1 to it
    count = 1
    for name in list_of_names:
        if entity == name.split("-")[0]:
            count += 1
    return count


def make_dict_with_info(images_file,model,names):
    # Making dictionary with name od entity, count, coords
    ideal_images_dir = {}
    for img in images_file:
        res = model(img)
        res = res[0]
        boxes = res.boxes
        ideal = []
        for box in boxes:
            entity = names[int(box.cls[0].item())].title()
            coords = str(box.xyxy[0].tolist())
            count = str(checkCount(entity, ideal))
            string = entity+"-"+count+"-"+coords
            ideal.append(string)
        ideal_images_dir[img.split("/")[-1]] = ideal

    return ideal_images_dir


def return_lists(given):
    list1 = []
    for i in given:
        if i.split("_")[0] not in list1:
            list1.append(i.split("-")[0])
    return list1


def need_in_other(ideal_dir):
    # Common things out of ideal photos
    list1 = return_lists(ideal_dir[list(ideal_dir.keys())[0]])
    list2 = return_lists(ideal_dir[list(ideal_dir.keys())[1]])
    return list(set(list1).intersection(list2))


def extra_in_other(ideal_dir):
    # Uncommon things out of ideal photos
    list1 = return_lists(ideal_dir[list(ideal_dir.keys())[0]])
    list2 = return_lists(ideal_dir[list(ideal_dir.keys())[1]])
    return list(set(list1).union(list2))


def missing_in_img(need, other_img):
    # Comparison between need_in_other and what is in other
    list1 = return_lists(other_img)
    missing = []
    for i in need:
        if i not in list1:
            missing.append(i)
    return missing


def extra_in_img(elim_extra, other_img):
    # Comparison between extra_eliminator and what is in other
    list1 = return_lists(other_img)
    extra = []
    for i in list1:
        if (i not in elim_extra) and (i not in extra):
            extra.append(i)
    return extra


def analyze(missing, extra, ideal_images_dir, other_image):
    # Figure out how to create a list of data to be written in csv file
    analysis = []
    for entity in missing:
        for i in list(ideal_images_dir.values()):
            for j in i:
                j = j.split("-")
                ideal_entity, coords = j[0], j[2]
                if entity == ideal_entity:
                    analysis.append([ideal_entity, "Missing", coords])
    for entity in extra:
        for i in other_image:
            if entity == i.split("-")[0]:
                coords = i.split("-")[2]
                analysis.append([entity, "Extra", coords])
    return analysis


def write_in_csv(path, result):
    # Make csv file and write in csv file
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in result:
            writer.writerow(row)


def main():
    # Initialise Problem & Output Folder
    directory = "Aithon/Ads_problem4/"
    output_path = "Aithon/problem4_output/"
    create_directory(output_path)
    folders = list_files(directory)

    model = load_pretrained_model()
    names = get_names()
    for folder in folders:
        # Initialise path for where folders are
        new_dir = directory+folder+"/"

        # Initialise path for where Ideal & Other folders are
        ideal_directory = new_dir+"Ideal/"
        other_directory = new_dir+"Other/"

        # Get List of files in that folder
        ideal_images = list_files(ideal_directory, ideal_directory)
        other_images = list_files(other_directory, other_directory)

        # Make a dictionary
        ideal_images_dir = make_dict_with_info(ideal_images,model,names)
        other_images_dir = make_dict_with_info(other_images,model,names)

        # Checking Missing & Extra
        need = need_in_other(ideal_images_dir)
        extra_eliminator = extra_in_other(ideal_images_dir)
        for key in list(other_images_dir.keys()):
            other_image = other_images_dir[key]
            missing = missing_in_img(need, other_image)
            extra = extra_in_img(extra_eliminator, other_image)
            result = [["Entity", "Difference", "Meta"]]
            result.extend(
                analyze(missing, extra, ideal_images_dir, other_image))

            path = output_path+key.split(".")[0]+".csv"
            write_in_csv(path, result)


if __name__ == "__main__":
    # Baseline 08.136742 seconds
    main()
