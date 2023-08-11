from ultralytics import YOLO
import os
import numpy as np
import torch
from PIL import Image
import clip
from datetime import datetime
start = datetime.now()


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


def cleancoords(coordinates):
    old_coords = coordinates[1:-1]
    old_coords = old_coords.split(".")
    new_coords = []
    for coord in old_coords:
        if "," not in coord:
            new_coords.append(int(coord.strip()))
        else:
            new_coords.append(int(coord.split(" ")[-1]))
    return new_coords


def crop_image(image, coords):
    coords = cleancoords(coords)
    coords = torch.tensor(coords)
    coords = np.array(coords)
    image_arr = np.array(image)
    xmin = int(coords[0])
    ymin = int(coords[1])
    xmax = int(coords[2])
    ymax = int(coords[3])
    crp = image_arr[ymin:ymax, xmin:xmax]
    return Image.fromarray(crp)


def get_top_three_indexes(listing):
    if len(listing) == 0:
        index1 =-100
        index2=-100
        index3=-100
        return index1,index2,index3
    elif len(listing) == 1:
        top1= max(listing)
        index1=listing.index(top1)
        index2,index3 = -100,-100
        return index1, index2, index3
    elif len(listing) == 2:
        top1=max(listing)
        index1=0
        index2=0
        top2=-1
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
        top1=max(listing)
        index1=0
        index2=0
        top2=-1
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


def simalirty_btw_images(image1, image2):
    image1_features = clip_model.encode_image(image1)
    image2_features = clip_model.encode_image(image2)
    # Normalize the vectors
    image1_features = torch.nn.functional.normalize(image1_features, dim=1)
    image2_features = torch.nn.functional.normalize(image2_features, dim=1)

    # Compute cosine similarity
    cos_sim = (image1_features @ image2_features.T).clamp(-1, 1)

    # Extract scalar value
    cos_sim = cos_sim.item()

    return cos_sim


def analyze(dictionary):
    # [image_name, entity, entity_count, cropped_image]
    for entities in list(dictionary.values()):
        for entity in entities:
            similar = []
            rating = []
            output_path_for_entity = output_path+entity[0]+"/"+entity[2] + "/"
            create_directory(output_path_for_entity)
            image1 = preprocess(entity[3]).unsqueeze(0).to('cpu')

            for similar_entity in entities:
                if similar_entity[0] != entity[0]:
                    image2 = preprocess(
                        similar_entity[3]).unsqueeze(0).to('cpu')
                    rating.append(simalirty_btw_images(image1, image2))
                    similar.append(similar_entity[3])
            i1, i2, i3 = get_top_three_indexes(rating)

            # Saving images
            entity[3].save(output_path_for_entity+entity[2]+"-crop.jpg")
            if i1 != -100:
                similar[i1].save(output_path_for_entity+"top1-crop.jpg")
            if i2!=-100:
                similar[i2].save(output_path_for_entity+"top2-crop.jpg")
            if i3!=-100:
                similar[i3].save(output_path_for_entity+"top3-crop.jpg")
            print(entity)


def main():
    dict_for_analyzing = {}
    count = 0
    for file in files:
        image_name = file.split(".")[0]
        filepath = output_path+image_name+"/"
        create_directory(filepath)

        res = model(directory+file)[0]
        boxes = res.boxes

        countDict = {}

        img = Image.open(directory+file)
        count += 1
        for box in boxes:

            entity = names[int(box.cls[0].item())]

            if entity in list(countDict.keys()):
                countDict[entity] += 1
            else:
                countDict[entity] = 1
            entity_count = names[int(box.cls[0].item())
                                 ].title() + str(countDict[entity])
            count += 1
            create_directory(filepath+entity_count)

            coords = str(box.xyxy[0].tolist())
            cropped_image = crop_image(img, coords)

            list_for_entity = [image_name, entity,
                               entity_count, cropped_image]

            if entity in list(dict_for_analyzing.keys()):
                old_list = dict_for_analyzing[entity]
                old_list.append(list_for_entity)
                dict_for_analyzing[entity] = old_list
            else:
                dict_for_analyzing[entity] = [list_for_entity]
    analyze(dict_for_analyzing)


directory = "Aithon/All_Images/"

files = list_files(directory)

model = load_pretrained_model()
names = get_names()

clip_model = clip.load("ViT-B/32", device='cpu')[0]
preprocess = clip.load("ViT-B/32", device='cpu')[1]

output_path = "Aithon/problem5_output/"
create_directory(output_path)

if __name__ == "__main__":
    # No. of entities 232
    # Baseline 17 minutes
    main()
    print(datetime.now()-start)
