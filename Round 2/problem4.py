from common_functions import list_files, load_pretrained_model, get_names
import csv

# Initialise Problem & Output Folder
directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/Ads_problem4/"
output = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem4_output/"

folders = list_files(directory)

model = load_pretrained_model()
names = get_names()


def checkCount(entity, list_of_names):
    count = 1
    for name in list_of_names:
        if entity == name.split("-")[0]:
            count += 1
    return count


def make_dict_with_info(images_file):
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
    list1 = return_lists(ideal_dir[list(ideal_dir.keys())[0]])
    list2 = return_lists(ideal_dir[list(ideal_dir.keys())[1]])
    return list(set(list1).intersection(list2))


def extra_in_other(ideal_dir):
    list1 = return_lists(ideal_dir[list(ideal_dir.keys())[0]])
    list2 = return_lists(ideal_dir[list(ideal_dir.keys())[1]])
    return list(set(list1).union(list2))


def missing_in_img(need, other_img):
    list1 = return_lists(other_img)
    missing = []
    for i in need:
        if i not in list1:
            missing.append(i)
    return missing


def extra_in_img(elim_extra, other_img):
    list1 = return_lists(other_img)
    extra = []
    for i in list1:
        if (i not in elim_extra) and (i not in extra):
            extra.append(i)
    return extra


def analyze(missing, extra, ideal_images_dir, other_image):
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
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        for row in result:
            writer.writerow(row)


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
    ideal_images_dir = make_dict_with_info(ideal_images)
    other_images_dir = make_dict_with_info(other_images)

    # FINAL CODE
    need = need_in_other(ideal_images_dir)
    extra_eliminator = extra_in_other(ideal_images_dir)
    for key in list(other_images_dir.keys()):
        other_image = other_images_dir[key]
        missing = missing_in_img(need, other_image)
        extra = extra_in_img(extra_eliminator, other_image)
        result = [["Entity", "Difference", "Meta"]]
        result.extend(analyze(missing, extra, ideal_images_dir, other_image))

        path = output+key.split(".")[0]+".csv"
        write_in_csv(path, result)

    # TODO:
    # ----------DONE need_in_other() ==> common things out of ideal photos
    # ----------DONE extra_in_other() ==> uncommon things out of ideal photos
    # ----------DONE missing_in_img() ==> comparison between need_in_other and what is in other
    # ----------DONE extra_in_img() ==> comparison between extra_eliminator and what is in other
    # ----------DONE analyze() ==> Figure out how to create a list of data to be written in csv file
    # ----------DONE write_in_csv() ==> make csv file and write in csv file
