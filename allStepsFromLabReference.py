# Import libraries
import cv2
import os
import numpy as np

# Make a copy
# Image path
# Change this path to your local folder
image_path = 'connector.png'
# Image directory
directory = 'saved_image/'
# Reading image
img = cv2.imread(image_path)
# Create the directory if it not exist
if not os.path.exists(directory):
    os.makedirs(directory)
# Change the current directory
# to specified directory
os.chdir(directory)
# List files and directories
print("Before saving image:")
print(os.listdir('.'))
# Filename
filename = 'saved_connector.png'
# Using cv2.imwrite() method
# Saving the image
cv2.imwrite(filename, img)
# List files and directories
print("After saving image:")
print(os.listdir('.'))
print('Successfully saved')

# Lines
path = r'saved_connector.png'
save_file = r'line_connector.png'
# Reading an image in default mode
image = cv2.imread(path)
# Window name in which image is displayed
window_name = 'Connector'
# Start coordinate, here (0, 0)
# represents the top left corner of image
start_point = (50, 50)
# End coordinate, here (250, 250)
# represents the bottom right corner of image
end_point = (270, 270)
# Green color in BGR
color = (0, 255, 0)
# Line thickness of 9 px
thickness = 9
# Using cv2.line() method
# Draw a diagonal green line with thickness of 9 px
image = cv2.line(image, start_point, end_point, color, thickness)
# Saving the image
cv2.imwrite(save_file, image)
# Displaying the image
cv2.imshow(window_name, image)
# Wait for user
cv2.waitKey(0)
# Close window and clear memory
cv2.destroyAllWindows()


# Name
path = r'line_connector.png'
save_file = r'text_connector.png'

# Reading an image in default mode
image = cv2.imread(path)
# Window name in which image is displayed
window_name = 'Connector with text'
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (130, 90)
# fontScale
fontScale = 1
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2
# Using cv2.putText() method
image = cv2.putText(image, 'Quor Zak', org, font, fontScale, color, thickness, cv2.LINE_AA)
# Saving the image
cv2.imwrite(save_file, image)
# Displaying the image
cv2.imshow(window_name, image)
# Wait for user
cv2.waitKey(0)
# Close window and clear memory
cv2.destroyAllWindows()

# colour change
path = r'text_connector.png'
save_file = r'gray_connector.png'

# Reading an image in default mode
src = cv2.imread(path)
# Window name in which image is displayed
window_name = 'Gray connector'
# Using cv2.cvtColor() method
# Using cv2.COLOR_BGR2GRAY color space
# conversion code
image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
# Displaying the image
cv2.imshow(window_name, image)
# Saving the image
cv2.imwrite(save_file, image)
# Wait for user
cv2.waitKey(0)
# Close window and clear memory
cv2.destroyAllWindows()

# thresholding
path = r'text_connector.png'
save_file = r'thresh_connector.png'
# Reading an image in default mode
image = cv2.imread(path)
# image is loaded with imread command
#image = cv2.imread(r'saved_images/gray_connector.png')
# cv2.cvtColor is applied over the
# image input with applied parameters
# to convert the image in grayscale
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#age = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
# applying different thresholding
# techniques on the input image
# all pixels value above 120 will
# be set to 255
ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(img, 120, 255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO)
ret, thresh5 = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO_INV)
# Join images together
thresh = np.concatenate((thresh1, thresh2, thresh3, thresh4, thresh5), axis=1)
# the window showing output images
# with the corresponding thresholding
# techniques applied to the input images
cv2.imshow('Binary, Binary Inverted, Truncated, Zero, Zero Inverted Threshold', thresh)
# Saving the image
cv2.imwrite(save_file, thresh)
# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()

# edge detection
img = cv2.imread(save_file)
save_file = r'edge_connector.png'

# Setting parameter values
t_lower = 50 # Lower Threshold
t_upper = 150 # Upper threshold
# Applying the Canny Edge filter
edge = cv2.Canny(img, t_lower, t_upper)
# Saving the image
cv2.imwrite(save_file, edge)
cv2.imshow('Edge', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()