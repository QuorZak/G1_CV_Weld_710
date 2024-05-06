###

###

# Import libraries
import cv2
import numpy as np
import os
import csv

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
    folder_path = 'C:\Users\inpal\OneDrive\Desktop\G1_CV_Weld_710\WeldGapImages\Set 1'

    bw_threshold_low = 120
    bw_maxVal = 255

    folder_name = "xxxx"
    other_name1 = "xxxx"
    other_name2 = "xxxx"
    other_name3 = "xxxx"



    # 1) read folder content and store in a list
    image_list = read_images_from_folder(folder_path)
    
    save_counter_bw = 0
    save_counter_cropped = 0
    save_counter_edge = 0
    # 2) for each image in list
    for image_name in image_list:
         # Convert the image to black and white
        bw_image = convert_to_black_and_white(image_name)
    # Display the black and white image (optional)
    # 3) do lots of processing steps, including saving imtermediate steps
    #ret, thresh1 = cv2.threshold(image, bw_threshold_low, bw_maxVal, cv2.THRESH_BINARY)
        ret, thresh = cv2.threshold(bw_image, bw_threshold_low, bw_maxVal, cv2.THRESH_TOZERO)

        line_color = (120, 255, 0)  # Green color in BGR format
        thickness = 2
        cv2.line(thresh, (0, 70), (thresh.shape[1], 70), line_color, thickness)

        mid_point = (int(thresh.shape[1]/2), 70)

        width_ROI = 1000
        height_ROI = 300
        x_ROI = max(mid_point[0] - width_ROI // 2, 0)
        y_ROI = max(mid_point[1] - height_ROI // 2, 0)
        cropped_image = thresh[y_ROI:y_ROI + height_ROI, x_ROI:x_ROI + width_ROI]

        t_lower = 500 # Lower Threshold
        t_upper = 850 # Upper threshold

        edge = cv2.Canny(cropped_image, t_lower, t_upper)

        cv2.imshow('zero_threshold', thresh)
        cv2.waitKey(0)  # Wait for any key press to continue to the next image
        


        if save_counter_bw < 3:  # Change the number to the desired amount of images to save
            save_path_bw = f"bw_image_{save_counter_bw}.png"  # You can change the file format if needed
            cv2.imwrite(save_path_bw, thresh)
            print(f"Saved BW image: {save_path_bw}")
            save_counter_bw += 1

        cv2.imshow('cropped_image', cropped_image)
        cv2.waitKey(0)  # Wait for any key press to continue to the next image

        if save_counter_cropped < 3:  # Change the number to the desired amount of images to save
            save_path_cropped = f"cropped_image_{save_counter_cropped}.png"  # You can change the file format if needed
            cv2.imwrite(save_path_cropped, cropped_image)
            print(f"Saved cropped image: {save_path_cropped}")
            save_counter_cropped += 1

        cv2.imshow('Edge', edge)
        cv2.waitKey(0)  # Wait for any key press to continue to the next image

        if save_counter_edge < 3:  # Change the number to the desired amount of images to save
            save_path_edge = f"cropped_image_{save_counter_edge}.png"  # You can change the file format if needed ##JPG-Requirement ##Cropped_image/Image
            cv2.imwrite(save_path_edge, edge)
            print(f"Edge detected image: {save_path_edge}")
            save_counter_edge += 1        

        
        if save_counter_bw >= 3 and save_counter_cropped >=3 and save_counter_edge >=3:
            break  # Exit the loop once the desired number of images have been saved
    

    

    # 4) store results in CSV + write final image

    # 5) at the end of the loop, write the CSV

    
        saved = []#initalising a list to save the data
        saved.append(save_path_edge,__)#insert weld gap position in pixel value
        if saved[1] > 0:
            saved.append(1)#Valid
        else:
            saved.append(0)#Invalid
        data = [saved]#data needs to be in an inner list to feed into CSV file
        with open('example.csv', 'w') as file:
            csv_writer = csv.writer(file)#initialising a writer object
            csv_writer.writerows(data)#inputting the data as each row into an table in the csv file



if __name__ == "__main__":
    main()