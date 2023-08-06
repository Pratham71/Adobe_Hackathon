# STRUCTURE
# 1) Loop through each image get list of entity and coordinte location
# 2) For{1} each entity in that image loop{2} through all the other images
#    with entity that is the same and and obtain similarity rating
# 3) Compare similarity as top 3 and make subfolder and paste cropped images in it

from common_functions import list_files, load_pretrained_model, get_names
import csv

# Initialise Problem & Output Folder
directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/All_Images/"
output = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem4_output/"

files = list_files(directory, directory)

model = load_pretrained_model()
names = get_names()


def checkCount(entity, list_of_names):
    count = 1
    for name in list_of_names:
        if entity == name.split("-")[0]:
            count += 1
    return count


def get_list_of_entity_with_coords(images_file):
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


def get_analyze_similarity(orginial_string, other_images_list):
    pass


list_with_file_entity_coords = get_list_of_entity_with_coords(files)
values = list(list_with_file_entity_coords.values())
for img_list in values:
    for string in img_list:
        entity = string.split("-")[0]
        similar_entities_list = []
        for similar_list in values:
            if img_list != similar_list:
                for similar_string in similar_list:
                    similar_entity = similar_string.split("-")[0]
                    if similar_entity == entity:
                        similar_entities_list.append(similar_string)
        get_analyze_similarity(string, similar_entities_list)
# TODO
# ----------DONE get_list_of_entity_with_coords() ==> get list of entities with their respective coordinates
# get_analyze_similarity() ==> get similarity between original entity and other images and
#                       get the top 3 with highest similarity
# crop_similarity() ==> crop the images from respective coordinates
# make_folder() ==> make a folder for respective enitity
# clip_images() ==> crop images with the highest similarity
# copy_to_folder() ==> copy images to their rescpective folder
