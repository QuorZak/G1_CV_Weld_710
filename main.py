###

###

# Import libraries
import cv2
import numpy as np
import os


# Do all our work, step by step, in here
def main():
    # Provide the path to the folder containing the images
    folder_path = '\Set 1'

    folder_name = "xxxx"
    other_name1 = "xxxx"
    other_name2 = "xxxx"
    other_name3 = "xxxx"

    bw_threshold_low = 120
    bw_maxVal= 255

    # 1) read folder content and store in a list
    image_list = read_images_from_folder(folder_path)
    

    # 2) for each image in list
    for image_name in image_list:
         # Convert the image to black and white
    bw_image = convert_to_black_and_white(image_file)
    # Display the black and white image (optional)
    cv2.imshow('Black and White Image', bw_image)
    cv2.waitKey(0)  # Wait for any key press to continue to the next image
        #image = cv2.imread(image_name)


    # 3) do lots of processing steps, including saving imtermediate steps
    ret, thresh1 = cv2.threshold(image, bw_threshold_low, bw_maxVal, cv2.THRESH_BINARY)




    # 4) store results in CSV + write final image

    # 5) at the end of the loop, write the CSV


if __name__ == "__main__":
    main()


#############################
# Create all functions here
#############################

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

                # Print the list of image files
    for image_file in image_files:
        print(image_file)

    return image_files

def convert_to_black_and_white(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


cv2.destroyAllWindows()


