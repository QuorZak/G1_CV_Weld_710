###

###

# Import libraries
import cv2
import numpy as np
import os

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


# Do all our work, step by step, in here
def main():
    # Provide the path to the folder containing the images
    folder_path = 'D:\Sem 2024\Mecheng 710\CV_Project\G1_CV_Weld_710\WeldGapImages\Set 1'

    bw_threshold_low = 120
    bw_maxVal = 255

    folder_name = "xxxx"
    other_name1 = "xxxx"
    other_name2 = "xxxx"
    other_name3 = "xxxx"



    # 1) read folder content and store in a list
    image_list = read_images_from_folder(folder_path)
    
    save_counter = 0
    # 2) for each image in list
    for image_name in image_list:
         # Convert the image to black and white
        bw_image = convert_to_black_and_white(image_name)
    # Display the black and white image (optional)
    # 3) do lots of processing steps, including saving imtermediate steps
    #ret, thresh1 = cv2.threshold(image, bw_threshold_low, bw_maxVal, cv2.THRESH_BINARY)
        ret, thresh = cv2.threshold(bw_image, bw_threshold_low, bw_maxVal, cv2.THRESH_TOZERO)


        if save_counter < 3:  # Change the number to the desired amount of images to save
            save_path = f"bw_image_{save_counter}.png"  # You can change the file format if needed
            cv2.imwrite(save_path, thresh)
            print(f"Saved image: {save_path}")
            save_counter += 1
        else:
            break  # Exit the loop once the desired number of images have been saved
    
    cv2.imshow('Zero Threshold', thresh)
    cv2.waitKey(0)  # Wait for any key press to continue to the next image

    

    # 4) store results in CSV + write final image

    # 5) at the end of the loop, write the CSV


if __name__ == "__main__":
    main()




