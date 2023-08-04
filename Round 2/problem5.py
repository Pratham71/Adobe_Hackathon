# STRUCTURE
# 1) Loop through each image get list of entity and coordinte location
# 2) For{1} each entity in that image loop{2} through all the other images 
#    with entity that is the same and and obtain similarity rating
# 3) Compare similarity as top 3 and make subfolder and paste cropped images in it

# TODO
# get_list_of_entity_with_coords() ==> get list of entities with their respective coordinates
# get_similarity() ==> get similarity between original entity and other image
# analyze_similarity() ==> get the top 3 with highes similarity
# crop_similarity() ==> crop the images from respective coordinates
# make_folder() ==> make a folder for respective enitity
# clip_images() ==> crop images with the highest similarity
# copy_to_folder() ==> copy images to their rescpective folder