# STRUCTURE
# 1) Loop through each image get list of entity and coordinte location
# 2) For{1} each entity in that image loop{2} through all the other images
#    with entity that is the same and and obtain similarity rating
# 3) Compare similarity as top 3 and make subfolder and paste cropped images in it

# TODO
# ----------DONE get_list_of_entity_with_coords() ==> get list of entities with their
#                respective coordinates
# ----------DONE make_folder() ==> make a folder for respective enitity
# ----------DONE return_folder_and_image_name() ==> returns name of folder
#                & name of image to save the picture in
# get_analyze_similarity() ==> get similarity between original entity and other images
#                              and get the top 3 with highest similarity
# crop_entity() ==> crop the images from respective coordinates
# Esstimate Time To Complete ==> 2 hours

from ultralytics import YOLO
import os
from PIL import Image


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
        "models/yolov8m.pt")
    model = YOLO(
        "models/yolov8l.pt")
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
    count = 1
    for name in list_of_names:
        if entity == name.split("-")[0]:
            count += 1
    return count


def get_list_of_entity_with_coords(images_file):
    # get list of entities with their respective coordinates
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
            string = entity+"-"+count+"-"+coords+"-"+img
            ideal.append(string)
        ideal_images_dir[img.split("/")[-1]] = ideal

    return ideal_images_dir


def return_folder_and_image_name(string, count=0):
    # returns name of folder
    # and name of image to save the picture in

    folder_name = ((string.split("-")[-1]).split(".")
                   [0]+"/").replace("All_Images", "problem5_output")
    entity = string.split("-")[0].lower()+string.split("-")[1]
    folder_name += entity
    if count == 0:
        img_name = folder_name+"/"+entity
    else:
        img_name = folder_name+"/"+"top"+str(count)
    return folder_name, img_name


def crop_entity(image):
    # Crop the images from respective coordinates
    pass


def get_analyze_similarity(orginal_string, other_images_list):
    # Get similarity between original entity and other images
    # and get the top 3 with highest similarity
    pass


# Initialise Problem & Output Folder
directory = "Aithon/All_Images/"

files = list_files(directory, directory)

model = load_pretrained_model()
names = get_names()

output_path = "Aithon/problem5_output/"
create_directory(output_path)

list_with_file_entity_coords = get_list_of_entity_with_coords(files)
values = list(list_with_file_entity_coords.values())

for img_list in values:
    for string in img_list:
        # Make a folder for respective image
        img_name = ((string.split("-")[-1]).split(".")
                    [0]+"/").replace("All_Images", "problem5_output")
        create_directory(img_name)
        entity = string.split("-")[0]
        entity_for_folder = string.split("-")[0].lower()+string.split("-")[1]

        # Make a folder for respective entity
        create_directory(img_name+entity_for_folder)

        # Initialise List
        similar_entities_list = []
        for similar_list in values:
            if img_list != similar_list:
                for similar_string in similar_list:
                    similar_entity = similar_string.split("-")[0]
                    if similar_entity != entity:
                        similar_entities_list.append(similar_string)
        get_analyze_similarity(string, similar_entities_list)
        print(similar_entities_list)
