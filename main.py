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

def read_image(image_path, read_type):
    # Read the image
    image = cv2.imread(image_path)
    # Convert the image if requested
    convert_image = cv2.cvtColor(image, read_type)
    return convert_image

def crop_roi(image, width_ROI = 1000, height_ROI = 300):
        mid_point = (int(image.shape[1]/2), 300)

        x_roi = max(mid_point[0] - width_ROI // 2, 0)
        y_roi = max(mid_point[1] - height_ROI // 2, 0)
        return image[y_roi:y_roi + height_ROI, x_roi:x_roi + width_ROI]

def adjust_thresholds(cropped, thresh1_low, thresh2_low):
    avg_brightness = np.mean(cropped)
    # Set2 = 60,45,20,10,15,15,40,40
    if avg_brightness > 220:  # Image is very bright
        thresh1_low += 60
        thresh2_low += 45
    elif avg_brightness > 180:  # Image is bright
        thresh1_low += 20
        thresh2_low += 10
    elif avg_brightness < 100:  # Image is dim
        thresh1_low -= 15
        thresh2_low -= 15
    elif avg_brightness < 50:  # Image is very dim
        thresh1_low -= 40
        thresh2_low -= 40

    thresh1_low = max(0, thresh1_low)
    thresh2_low = max(0, thresh2_low)

    return thresh1_low, thresh2_low

def abs_to_cropped_coords(image, coords):
    width_ROI = 1000
    #height_ROI = 300

    mid_point = (int(image.shape[1]/2), 300)
    x_roi = max(mid_point[0] - width_ROI // 2, 0)
    new_coords = []
    for coord in coords:
        new_coords.append(coord[0]-x_roi, coord[1], coord[2])
    return new_coords

def save_interim_images(image_array=[], total_image_count=1, folder_path='InterimResults/'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    os.chdir(folder_path)

    for interim_count, image in enumerate(image_array):
        name_string = f"Image{total_image_count:04}_B_InterimResult{interim_count+1}.jpg"
        cv2.imwrite(name_string, image)

    os.chdir('..')

def get_canny_line_centers(image, max_gap, y_location=70):
        x_positions = []
        begin_count = 0
        found_gap = False
        in_white_line = False
        for x_index, pixel_value in enumerate(image[y_location,:]): #just one scan line across y=70
            if pixel_value >= 250:  # find white lines
                if begin_count == 0 and not in_white_line:
                    begin_count = x_index
                    in_white_line = True
                elif found_gap == False:
                    pass
                else:
                    if (x_index-begin_count <= max_gap) and (x_index-begin_count > 1):
                        x_positions.append(((int(begin_count+x_index)/2),int(y_location),int(x_index-begin_count)))
                    begin_count = 0
                    found_gap = False
                    in_white_line = True
            elif pixel_value <= 5:
                if begin_count != 0 and found_gap == False:
                    found_gap = True
                    in_white_line = False
                elif in_white_line:
                    in_white_line = False

        return x_positions

def center_from_canny_pairs(edge, centers):
    best_center = (-1, -1, -1)
    best_count = 0
    for x, y, w in centers:
        count = 0
        current_x, current_y = x, y

        while edge[int(current_y),int(current_x)] <= 255 and current_y > 0: # array access is y then x
            count += 1
            current_y -= 1

        if count > best_count:
            best_count = count
            best_center = (int(x), int(y), int(w))

    return best_center

def center_from_darkest_pixel_and_height(thresh1, centers):
    best_center = (-1, -1, -1)
    darkest_line = 255
    min_count = 10
    for x, y, w in centers:
        count = 0
        current_x, current_y = x, y
        current_pixel = thresh1[int(current_y),int(current_x)] # array access is y then x

        while current_pixel <= 220 and current_y > 0:
            count += 1
            current_y -= 1

        if count > min_count:
            if current_pixel < darkest_line:
                best_center = (int(x), int(y), int(w))
                darkest_line = current_pixel

    return best_center

def draw_center_line(array, weld_center):
    # draw main line
    line_color = (120, 255, 0)  # Green color in BGR format
    cv2.line(array, (0, weld_center[1]), (array.shape[1], weld_center[1]), line_color, thickness=2)
    # draw highlight
    line_color = (0, 100, 200)  # Orange color in BGR format
    cv2.line(array, (int(weld_center[0]-(weld_center[2]/2))+1, weld_center[1]), (int(weld_center[0]+(weld_center[2]/2)), weld_center[1]), line_color, thickness=3)

def write_csv(write_list, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file) #initialising a writer object
        csv_writer.writerow(write_list) #inputting the data as each row into an table in the csv file

def save_final_image(image, total_image_count, folder_path='InterimResults/'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    os.chdir(folder_path)

    name_string = f"Image{total_image_count:04}_A_WeldGapPosition.jpg"
    cv2.imwrite(name_string, image)

    os.chdir('..')

###########################################
# Perform the functions step by step here
###########################################
def main():
    # Constants and global parameters
    max_weld_gap = 11 # 0.5 mm = 11 pixels
    pixel_width = 0.04607 # mm / pixel

    y_scan_location = 70
    roi_width, roi_height = 750, 140

    image_results = []

    source_folder_path = 'WeldGapImages/Set 1'
    interim_folder_path = 'InterimResults/'
    csv_filename = 'WeldGapPositions.csv'

    read_type1 = cv2.IMREAD_COLOR
    read_type2 = cv2.COLOR_BGR2GRAY

    thresh_type1 = cv2.THRESH_TRUNC
    thresh1_low, thresh1_maxVal = 130, 250 #set1 = 120, 250

    thresh_type2 = cv2.THRESH_BINARY
    thresh2_low, thresh2_maxVal = 90, 250 #set1 = 90, 250

    canny_thresh_lower = 150 #set1 = 100
    canny_thresh_upper = 200 #set1 = 200
    canny_hough_thresh = 50

    sobel_low = 200
    sobel_high = 255
    sobel_hough_thresh = 70

    show = False

    sobel = True

    using_hough_lines = False

    # 1) set up the interim folder then read source folder content  
    image_list = read_images_from_folder(source_folder_path)

    image_results = []
    
    # 2) for each image in list
    for current_image_index, image_name in enumerate(image_list, start=1):
         # Convert the image to black and white
        initial_image = read_image(image_name, read_type1)

    # 2a) scan the zone around the line to get the image average values and try to adjust thresholds
        cropped = crop_roi(initial_image, roi_width, roi_height)
        grey_image = cv2.cvtColor(cropped, read_type2)

        grey_copy = np.copy(grey_image)
        sobel_grey_copy = np.copy(grey_image)

        gauss = cv2.GaussianBlur(grey_image, (5, 5), 0)

        # also consider cv2.adaptive_tresholding()
        #thresh1_low, thresh2_low = adjust_thresholds(grey_image, thresh1_low, thresh2_low)
        
    # 3) do lots of processing steps, including saving interim steps
        ret, thresh0 = cv2.threshold(gauss, thresh1_low, thresh1_maxVal, thresh_type1) # trunc

        thresh1 = cv2.adaptiveThreshold(thresh0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 4)

        if sobel == True:
            sobel_x = cv2.Sobel(thresh1, cv2.CV_64F, 1, 0, ksize=1)
    
            # Convert to absolute values
            abs_sobel_x = cv2.convertScaleAbs(sobel_x)

            # Thresholding to isolate strong vertical edges
            ret, sobel_vert = cv2.threshold(abs_sobel_x, sobel_low, sobel_high, cv2.THRESH_BINARY)
            sobel_hough = cv2.HoughLinesP(sobel_vert, 1, np.pi/180, sobel_hough_thresh, None, 20, 2)

            sobel_saved_lines = []
            # draw sobel hough lines
            if sobel_hough is not None and len(sobel_hough) > 0:
                min_angle = 85  # 90 - 5
                max_angle = 95  # 90 + 5
                for line in sobel_hough:
                    x1, y1, x2, y2 = line[0]
                    theta_degrees = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                    if min_angle <= abs(theta_degrees) <= max_angle:
                        lin = line[0]
                        sobel_saved_lines = line
                        cv2.line(sobel_grey_copy, (lin[0], lin[1]), (lin[2], lin[3]), (0,0,255), 3, cv2.LINE_AA)

        #ret, thresh2 = cv2.threshold(thresh1, thresh2_low, thresh2_maxVal, thresh_type2) # binary

        #thresh2 = cv2.adaptiveThreshold(thresh1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        #maybe do sobel for y only?
        #edge = cv2.Sobel(thresh2, canny_thresh_lower, canny_thresh_upper)
        edge = cv2.Canny(thresh1, canny_thresh_lower, canny_thresh_upper)
        lines = cv2.HoughLinesP(edge, 1, np.pi/180, canny_hough_thresh, None, 40, 12)
        saved_lines = []
        # draw hough lines
        if lines is not None and len(lines) > 0:
            min_angle = 85  # 90 - 5
            max_angle = 95  # 90 + 5
            for line in lines:
                x1, y1, x2, y2 = line[0]
                theta_degrees = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                if min_angle <= abs(theta_degrees) <= max_angle:
                    lin = line[0]
                    saved_lines = line
                    cv2.line(grey_copy, (lin[0], lin[1]), (lin[2], lin[3]), (0,0,255), 3, cv2.LINE_AA)

        if show == True:
            cv2.imshow('threshold type 1', thresh1)
            cv2.waitKey(0)  # Wait for any key press to continue to the next image

            # cv2.imshow('gauss', gauss)
            # cv2.waitKey(0)  # Wait for any key press to continue to the next image

            #cv2.imshow('threshold type 2', thresh2)
            #cv2.waitKey(0)  # Wait for any key press to continue to the next image

            cv2.imshow('Edge', edge)
            cv2.waitKey(0)  # Wait for any key press to continue to the next image

            cv2.imshow('Hough Lines', grey_copy)
            cv2.waitKey(0)  # Wait for any key press to continue to the next image
     
        interim_images = [thresh1, sobel_vert, sobel_grey_copy, edge, grey_copy]
        save_interim_images(interim_images, current_image_index, interim_folder_path)

    # 5) detect and collect the weld gap x coordinates
        if not using_hough_lines:
            center_positions = get_canny_line_centers(edge, max_weld_gap, y_scan_location)   
            weld_center = -1
            valid = 0
            if len(center_positions) > 0:
                #weld_center = center_from_canny_pairs(edge, center_positions)
                weld_center = center_from_darkest_pixel_and_height(thresh1, center_positions)
                if weld_center[0] != -1:
                    draw_center_line(cropped, weld_center)
                    valid = 1  
        else: 
            weld_center = -1
            valid = 0
            if len(sobel_saved_lines) > 0:
                weld_center = center_from_hough_lines(sobel_saved_lines)
                if weld_center[0] != -1:
                    draw_center_line(cropped, weld_center)
                    valid = 1          
        
        image_results.append(f"Image{current_image_index:04}.jpg,{weld_center},{valid}") # format the results entry


    # 6) at the end of the loop, write the CSV and final image
        write_csv(image_results, csv_filename)
        save_final_image(cropped, current_image_index, interim_folder_path)


if __name__ == "__main__":
    main()