from common_functions import list_files
from ultralytics import YOLO
from common_functions import list_files, load_pretrained_model, get_names, read_file, list_of_entities, create_directory, delete_runs


directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/Ads_problem4/"
output = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem4_output/"
first_folder = list_files(directory)[0]
folders = []
folders.append(first_folder)
folders = list_files(directory)
model = load_pretrained_model()
names = get_names()


def predict_and_return_list(path_of_image):
    # Predicting for each image
    res = model(path_of_image, save_txt=True)

    # Reading file
    info = read_file(img, res[0])

    # Making List of Entities in Image
    return (list_of_entities(info, names))


for folder in folders:
    new_dir = directory+folder+"/"
    ideal_dir = new_dir+"Ideal/"
    other_dir = new_dir+"Other/"
    ideal_images = list_files(ideal_dir)
    other_images = list_files(other_dir)
    ideal_images_list = []
    other_images_list = []

    for img in ideal_images:
        ideal_images_list.append(predict_and_return_list(ideal_dir+img))

    for img in other_images:
        other_images_list.append(predict_and_return_list(other_dir+img))
