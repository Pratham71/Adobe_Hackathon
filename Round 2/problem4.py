from common_functions import list_files, load_pretrained_model, get_names, list_of_entities, get_info_using_res


directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/Ads_problem4/"
output = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem4_output/"

first_folder = list_files(directory)[0]
folders = []
folders.append(first_folder)


model = load_pretrained_model()
names = get_names()


def predict_and_return_list(path_of_image):
    # Predicting for each image
    res = model(path_of_image, save_txt=True)

    # Reading file
    info = get_info_using_res(res[0])

    # Making List of Entities in Image
    return (list_of_entities(info, names))


def common(ideal_list):
    return list(set(ideal_list[0]).intersection(ideal_list[1]))


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

    common_list = common(ideal_images_list)
    print(ideal_images_list)
    print(common_list)
    for img in other_images:
        list_entities = predict_and_return_list(other_dir+img)
