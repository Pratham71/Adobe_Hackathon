# METHOD USED for problem 5
# 1) Making folders for each image and in that sub folders for its entities
# 2) Crop all similar entities and save them in respective folder
# 3) Analyze TOP 3 similar entities
# 4) Rename TOP 3 similar entities
# 5) Delete not similar entities

from ultralytics import YOLO
from PIL import Image
import os
import numpy as np
import torch
import clip
import cv2


def list_files(directory, external=""):
    # list to store files
    res = [extrenal+file_path for file_path in os.listdir(directory)]

    # Iterate directory
    '''for file_path in os.listdir(directory):
        # add filename to list
        res.append(external+file_path)'''
    return res


def load_pretrained_model(weights):
    # load a pretrained model
    model=Yolo(weigths)
    '''model = YOLO(
        "models/yolov8n.pt")
    model = YOLO(
        "models/yolov8m.pt")
    model = YOLO(
        "models/yolov8l.pt")
    model = YOLO(
        "models/yolov8s.pt")'''
    return model


def get_names():
    model = load_pretrained_model()
    res = model(source="https://ultralytics.com/images/bus.jpg")
    return (res[0].names)


def create_directory(entity):
    #path = entity
    isExist = os.path.exists(entity)
    if not isExist:
        os.makedirs(entity)


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
        res = model(img)[0]
        #res = res[0]
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


def clean_coords(coordinates):
    old_coords = coordinates[1:-1].split(".")
    #old_coords = old_coords.split(".")
    new_coords = []
    for coord in old_coords:
        if "," not in coord:
            new_coords.append(int(coord.strip()))
        else:
            new_coords.append(int(coord.split(" ")[-1]))
    return new_coords


def crop_entity(image, coordinates, save_path):
    # Security Measure
    coords = clean_coords(coordinates)

    # Converting into Tensor Coordinates
    coords = torch.tensor(coords)
    coords = np.array(coords)
    i = cv2.imread(image)
    xmin = int(coords[0])
    ymin = int(coords[1])
    xmax = int(coords[2])
    ymax = int(coords[3])
    # Crop image
    cropped_image = i[ymin:ymax, xmin:xmax]

    # Save cropped image
    cv2.imwrite(save_path, cropped_image)


def crop_lists(original, lists_of_images, path):
    org_img, org_coords, org_path = original.split(
        "-")[-1], original.split("-")[2], path+original.split("-")[0].lower()+original.split("-")[1]+"-crop.jpg"
    crop_entity(org_img, org_coords, org_path)
    count = 1
    for img in lists_of_images:
        org_img, org_coords, org_path = img.split(
            "-")[-1], img.split("-")[2], path+str(count)+".jpg"
        crop_entity(org_img, org_coords, org_path)
        count += 1


def rename(top1_name, top2_name, top3_name, path):
    path = os.getcwd().replace("\\", "/")+"/"+path
    os.rename(path+top1_name, path+"top1-crop.jpg")
    os.rename(path+top2_name, path+"top2-crop.jpg")
    if not top3_name:
        pass
    else:
        os.rename(path+top3_name, path+"top3-crop.jpg")


def delete(path, files):
    path = os.getcwd().replace("\\", "/")+"/"+path
    for file in files:
        if "-crop" not in file:
            os.remove(path+file)


def similarity_bwt_two_pictures(image1, image2):

    image1_features = clip_model.encode_image(image1)
    image2_features = clip_model.encode_image(image2)
    return (clip.cosine_similarity(image1_features, image2_features).item())
    # return image1_features.cosine_similarity(image2_features).item()


def get_top_three_indexes(listing):
    top1 = max(listing)
    top2 = -1
    index1,index2=0,0
    #index2 = 0
    if len(listing) == 2:
        index3 = -100
        count = 0
        for num in listing:
            if num == top1:
                index1 = count
            elif num > top2:
                top2 = num
                index2 = count
            count += 1
        return index1, index2, index3
    else:
        top3 = -1
        index3 = 0
        count = 0
        for num in listing:
            if num == top1:
                index1 = count
            elif num > top2:
                top2 = num
                index2 = count
            elif num > top3:
                top3 = count
                index3 = count
            count += 1
        return index1, index2, index3


def analyze(path, files):
    similar = []
    similarity = []
    for file in files:
        img = Image.open(path+file)
        if "-crop" in file:
            original = preprocess(img)
            original = original.unsqueeze(0).to('cpu')
        else:
            pic = preprocess(img)
            pic = pic.unsqueeze(0).to('cpu')
            similar.append(pic)
    for image in similar:
        similarity.append(similarity_bwt_two_pictures(original, image))
    i1, i2, i3 = get_top_three_indexes(similarity)
    if i3 == -100:
        return files[i1], files[i2], False
    else:
        return files[i1], files[i2], files[i3]


def analyze_similarity(path):
    # Get similarity between original entity and other images
    # and get the top 3 with highest similarity
    files = list_files(path)
    if len(files) == 1:
        pass
    elif len(files) == 2:
        for file_name in files:
            if "-crop" not in file_name:
                os.rename(path+file_name, path+"top1-crop.jpg")
    else:
        top1_name, top2_name, top3_name = analyze(path, files)
        rename(top1_name, top2_name, top3_name, path)
        delete(path, list_files(path))


# Initialise Problem & Output Folder
directory = "Aithon/All_Images/"

files = list_files(directory, directory)

model = load_pretrained_model()
names = get_names()

clip_model = clip.load("ViT-B/32", device='cpu')[0]
preprocess = clip.load("ViT-B/32", device='cpu')[1]

output_path = "Aithon/problem5_output/"
create_directory(output_path)

list_with_file_entity_coords = get_list_of_entity_with_coords(files)
values = list(list_with_file_entity_coords.values())


def main():
    for img_list in values:
        for string in img_list:
            # Make a folder for respective image
            img_name = ((string.split("-")[-1]).split(".")
                        [0]+"/").replace("All_Images", "problem5_output")
            create_directory(img_name)
            entity = string.split("-")[0]
            entity_for_folder = string.split(
                "-")[0].lower()+string.split("-")[1]

            # Make a folder for respective entity
            create_directory(img_name+entity_for_folder)

            # Initialise List
            similar_entities_list = []
            for similar_list in values:
                if img_list != similar_list:
                    for similar_string in similar_list:
                        similar_entity = similar_string.split("-")[0]
                        if similar_entity == entity:
                            similar_entities_list.append(similar_string)
            crop_lists(string, similar_entities_list,
                       img_name+entity_for_folder+"/")
            analyze_similarity(img_name+entity_for_folder+"/")


if __name__ == "__main__":
    main()
    # Baseline 23 mins 23.269339 seconds
