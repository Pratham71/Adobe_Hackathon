from PIL import Image
from common_functions import load_pretrained_model, list_files


def main():

    model = load_pretrained_model()

    # Classifing Directory
    directory = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/Aithon/All_Images/"

    # Getting list of flies
    image_list = list_files(directory)

    # Iterating over list
    for img in image_list:
        # Predicting for each image
        res = model.predict(str(directory+img))[0]

        res = res.plot(line_width=1)
        res = res[:, :, ::-1]

        # Making boxes
        res = Image.fromarray(res)

        # Saving file in destination
        destination = "C:/Users/allof/Downloads/Timepass/Adobe Hackathon/Round 2/OUTPUT/problem1_output/"+img
        res.save(destination)


if __name__ == "__main__":
    main()
