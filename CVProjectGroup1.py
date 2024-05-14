'''
This Python files takes in a series of images from a specified folder and reads them using CV2.imread().
It then attempts to find a narrow, dark, vertical gap in the image which has so far been a weld gap for insutrial purposes.
It writes the results of the center of these weld gaps as 'x' at y=70 into a CSV. It also saves some interim image results.
'''

# Import libraries
import cv2
import numpy as np
import os
import csv

#############################
# All functions
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
    # these values were set manually. They're subjective and not perfect
    if avg_brightness > 220:  # Image is very bright
        thresh1_low += 20
        thresh2_low += 20
    elif avg_brightness > 180:  # Image is bright
        thresh1_low += 10
        thresh2_low += 10
    elif avg_brightness < 100:  # Image is dim
        thresh1_low -= 5
        thresh2_low -= 5
    elif avg_brightness < 50:  # Image is very dim
        thresh1_low -= 15
        thresh2_low -= 15
    # avoid setting below 0
    thresh1_low = max(0, thresh1_low)
    thresh2_low = max(0, thresh2_low)
    return thresh1_low, thresh2_low

def group_by_contrast(image):
    thresholds = [0, 50, 100, 150, 200, 225] 
    result = np.zeros_like(image)
    # Assigning new values based on thresholds
    result[image <= thresholds[0]] = 0
    result[(image > thresholds[0]) & (image <= thresholds[1])] = 25
    result[(image > thresholds[1]) & (image <= thresholds[2])] = 75
    result[(image > thresholds[2]) & (image <= thresholds[3])] = 125
    result[(image > thresholds[3]) & (image <= thresholds[4])] = 175
    result[(image > thresholds[4]) & (image <= thresholds[5])] = 225
    result[(image > thresholds[5])] = 255
    return result

def draw_hough_lines(display_image, lines):
    saved_lines = []
    if lines is not None and len(lines) > 0:
        min_angle = 85  # 90 - 5
        max_angle = 95  # 90 + 5
        for line in lines:
            x1, y1, x2, y2 = line[0]
            theta_degrees = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            if min_angle <= abs(theta_degrees) <= max_angle:
                lin = line[0]
                saved_lines = line
                cv2.line(display_image, (lin[0], lin[1]), (lin[2], lin[3]), (0,0,255), 3, cv2.LINE_AA)
    return saved_lines

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

def check_for_hough_cluster(lines, width_thresh=12):
    # extract x positions and initalise
    x_positions = []
    for line in lines:
        x_positions.append(line[0])
    x_positions.sort()
    clusters = []
    current_cluster = [x_positions[0]]
    # get all sequential positions
    for x in x_positions[1:]:
        if x - current_cluster[0] <= width_thresh:
            current_cluster.append(x)
        else:
            if len(current_cluster) > 1:
                clusters.append(current_cluster)
            current_cluster = [x]
    # Add the last cluster
    if len(current_cluster) > 1:
        clusters.append(current_cluster)
    # if only 1 cluster, return cluster average x
    if len(clusters) == 1:
        return np.mean(clusters[0])
    else:
        return -1
    

def get_canny_line_centers(image, max_gap, lines, y_location=70):
        x_positions = []
        begin_count = 0
        found_gap = False
        in_white_line = False
        for x_index, pixel_value in enumerate(image[y_location,:]): #just one scan line across y=70
            if pixel_value >= 245:  # find white lines
                if begin_count == 0 and not in_white_line:
                    begin_count = x_index
                    in_white_line = True
                elif found_gap == False:
                    pass
                else:
                    x_average = int(int(begin_count+x_index)/2)
                    if (x_index-begin_count <= max_gap) and (x_index-begin_count > 1) and if_near_hought(x_average, lines):
                        x_positions.append((x_average,int(y_location),int(x_index-begin_count)))
                    begin_count = 0
                    found_gap = False
                    in_white_line = True
            elif pixel_value <= 10: # find black pixels
                if begin_count != 0 and found_gap == False:
                    found_gap = True
                    in_white_line = False
                elif in_white_line:
                    in_white_line = False

        return x_positions

def if_near_hought(x, lines):
    if lines is not None and len(lines) > 0:
        for line in lines:
            x1, y1, x2, y2 = line[0],line[1],line[2],line[3]
            diff = int(abs(x-((x1+x2)/2)))
            if (diff < 10):
                return True
    return False


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

def center_from_darkest_pixel_and_height(edge, centers):
    best_center = (-1, -1, -1)
    darkest_line = 255
    min_count = 10
    for x, y, w in centers:
        count = 0
        current_x, current_y = x, y
        current_pixel = edge[int(current_y),int(current_x)] # array access is y then x

        while current_pixel <= 220 and current_y > 0:
            count += 1
            current_y -= 1

        if count > min_count:
            if current_pixel < darkest_line:
                best_center = (int(x), int(y), int(w))
                darkest_line = current_pixel

    return best_center

def center_from_darkest_hough_line(array, lines):
    darkest_line = 256
    best_point = (-1,-1,-1)
    valid = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if (y1 <= 70 <= y2) or (y2 <= 70 <= y1):
            if array[70,x1] < darkest_line:
                darkest_line = array[70,x1]
                best_point = (x1,70,7)
    if best_point[0] != -1:
        valid = 1
    return best_point, valid

def draw_center_line(array, weld_center):
    # draw main line
    line_color = (120, 255, 0)  # Green color in BGR format
    cv2.line(array, (0, weld_center[1]), (array.shape[1], weld_center[1]), line_color, thickness=2)
    # draw highlight
    line_color = (0, 100, 200)  # Orange color in BGR format
    cv2.line(array, (int(weld_center[0]-(weld_center[2]/2))+1, weld_center[1]), (int(weld_center[0]+(weld_center[2]/2)), weld_center[1]), line_color, thickness=3)

def write_csv(write_list, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        for item in write_list:
            csv_file.write(item + '\n')

def save_final_image(image, total_image_count, folder_path='InterimResults/'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    os.chdir(folder_path)
    name_string = f"Image{total_image_count:04}_A_WeldGapPosition.jpg"
    cv2.imwrite(name_string, image)
    os.chdir('..')

###########################################
# Main Function
###########################################
def main():
    # Constants and global parameters
    max_weld_gap = 11 # 0.5 mm = 11 pixels
    pixel_width = 0.04607 # mm / pixel

    y_scan_location = 70
    roi_width, roi_height = 750, 150

    image_results = []

    source_folder_path = 'WeldGapImages/Set 3'
    interim_folder_path = 'InterimResults/'
    csv_filename = 'WeldGapPositions.csv'

    read_type1 = cv2.IMREAD_COLOR
    read_type2 = cv2.COLOR_BGR2GRAY

    thresh_type1 = cv2.THRESH_BINARY
    thresh1_low, thresh1_maxVal = 75, 250 #set1 = 75, 250

    thresh_type2 = cv2.THRESH_TRUNC
    thresh2_low, thresh2_maxVal = 120, 250 #set1 = 120, 250

    canny1_thresh_lower = 150 #set1 = 150 - not for hough - binary
    canny1_thresh_upper = 250 #set1 = 250 - not for hough - binary

    canny2_thresh_lower = 150 #set1 = 150
    canny2_thresh_upper = 250 #set1 = 250

    show = False

    using_edge2 = True

    ###########################################
    # Perform the functions step by step here
    ###########################################
    # # 1) set up the interim folder then read source folder content  
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

        thresh1_low, thresh2_low = adjust_thresholds(grey_image, thresh1_low, thresh2_low)
        
    # 3) do lots of processing steps, including saving interim steps
        gauss = cv2.GaussianBlur(grey_image, (7, 7), 0)

        clahe_param = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(10, 10))
        contrast = clahe_param.apply(gauss)

        grouped = group_by_contrast(gauss)

        edge2 = cv2.Canny(grouped, canny2_thresh_lower, canny2_thresh_upper)

        ret, thresh1 = cv2.threshold(contrast, contrast.min()+(thresh1_low/3), thresh1_maxVal, thresh_type1) # binary

        edge1 = cv2.Canny(thresh1, canny1_thresh_lower, canny1_thresh_upper)

        lines = cv2.HoughLinesP(edge1, 1, np.pi/180, 50, None, 40, 12)
        saved_lines = draw_hough_lines(grey_copy, lines)

        interim_images = [contrast, thresh1, edge1, grouped, edge2, grey_copy]
        save_interim_images(interim_images, current_image_index, interim_folder_path)

    # 5) detect and collect the weld gap x coordinates
        valid1 = 0
        weld_center1 = (-1,-1,-1) #(x,y,width)
        center_positions1 = get_canny_line_centers(edge1, max_weld_gap, saved_lines, y_scan_location) #binary
        if len(center_positions1) > 0:
            #weld_center = center_from_canny_pairs(edge, center_positions)
            weld_center1 = center_from_darkest_pixel_and_height(contrast, center_positions1)
            if weld_center1[0] != -1:
                valid1 = 1

        if using_edge2:
            valid2 = 0
            weld_center2 = -1
            center_positions2 = get_canny_line_centers(edge2, max_weld_gap, saved_lines, y_scan_location) #groups
            if len(center_positions2) > 0:
                weld_center2 = center_from_darkest_pixel_and_height(contrast, center_positions2) # use gauss or contrast
                if weld_center2[0] != -1:
                    valid2 = 1

        # final decision making
        if valid1:
            draw_center_line(cropped, weld_center1)
            image_results.append(f"Image{current_image_index:04}.jpg,{weld_center1[0]},{valid1}") # format the results entry
        elif valid2:
            draw_center_line(cropped, weld_center2)
            image_results.append(f"Image{current_image_index:04}.jpg,{weld_center2[0]},{valid2}")
        elif saved_lines is not None and len(saved_lines) > 0:
            # single hough cluster method
            x_cluster = check_for_hough_cluster(saved_lines)
            weld_center3, valid3 = center_from_darkest_hough_line(contrast, lines)
            if x_cluster != -1:
                draw_center_line(cropped, (x_cluster,70,7))
                image_results.append(f"Image{current_image_index:04}.jpg,{x_cluster},{1}")

            # best guess hough method
            elif valid3:
                
                draw_center_line(cropped, weld_center3)
            image_results.append(f"Image{current_image_index:04}.jpg,{weld_center3[0]},{valid3}")
        else:
            image_results.append(f"Image{current_image_index:04}.jpg,{weld_center1[0]},{valid1}")

    # 6) at the end of the loop, write the CSV and final image
        write_csv(image_results, csv_filename)
        save_final_image(cropped, current_image_index, interim_folder_path)

        if show == True:
            cv2.imshow('threshold type 1', thresh1)
            cv2.waitKey(0)  # Wait for any key press to continue to the next image

            # cv2.imshow('threshold type 2', thresh2)
            # cv2.waitKey(0)  # Wait for any key press to continue to the next image

            cv2.imshow('Edge', edge1)
            cv2.waitKey(0)  # Wait for any key press to continue to the next image


if __name__ == "__main__":
    main()