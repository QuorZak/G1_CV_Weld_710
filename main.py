###

###

# Import libraries
import cv2
import numpy as np
import os

def read_images_from_folder(folder_path):
    image_files = []
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']  # Add more extensions if needed

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a supported image extension
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            # Form the full path of the image file
            image_path = os.path.join(folder_path, filename)
            # Add the image path to the list
            image_files.append(image_path)

    return image_files

# Provide the path to the folder containing the images
folder_path = 'D:\Sem 2024\Mecheng 710\WeldGapImages\Set 1'

# Get the list of image files
image_files_list = read_images_from_folder(folder_path)

# Print the list of image files
for image_file in image_files_list:
    print(image_file)


# Do all our work, step by step, in here
def main():
    folder_name = "xxxx"
    other_name1 = "xxxx"
    other_name2 = "xxxx"
    other_name3 = "xxxx"

    # 1) read folder content and store in a list
    image_list = []
    

    # 2) for each image in list
    for image_name in image_list:
        image = cv2.imread(image_name)


    # 3) do lots of processing steps, including saving imtermediate steps


    # 4) store results in CSV + write final image

    # 5) at the end of the loop, write the CSV


if __name__ == "__main__":
    main()