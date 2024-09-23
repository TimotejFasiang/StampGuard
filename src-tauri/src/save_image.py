import sys
import cv2
import os
import numpy as np


def save_image(image_path):
    original_image = cv2.imread(image_path)

    # Define the output directory in the .local/share/stamp-guard path
    home_dir = os.path.expanduser("~")
    output_dir = os.path.join(home_dir, ".local", "share", "stamp-guard", "frontend")

    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist, creating it.")
        os.makedirs(output_dir)

    output_path_orig = os.path.join(output_dir, 'orig_image.jpg')
    success_orig = cv2.imwrite(output_path_orig, original_image)
    if not success_orig:
        print(f"Failed to write original image to {output_path_orig}")
    else:
        print(f"Original image saved successfully to {output_path_orig}")

    #############################################################
    #################### IMAGE EDITING Start ####################
    #############################################################

    # Step 1: Convert to HSV color space
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # Step 2: Define the lower and upper bounds for black in HSV
    # Bounds for black (Hue = any, Saturation = 0 to very low, Value = 0 to low)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([50, 15, 10])  # Adjust the upper limit based on testing

    # Step 3: Create a mask to extract black regions
    mask = cv2.inRange(hsv, lower_black, upper_black)
    # # Step 4: Optional - Morphological operations to clean the mask
    # kernel = np.ones((3, 3), np.uint8)
    # mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Step 6: Invert the mask to get black text on a white background
    # mask_inverted = cv2.bitwise_not(mask)

    # Step 5: Apply the mask to the original image
    result = cv2.bitwise_and(original_image, original_image, mask=mask)

    ###########################################################
    #################### IMAGE EDITING End ####################
    ###########################################################

    output_path_edit = os.path.join(output_dir, 'processed_image.jpg')
    success_edit = cv2.imwrite(output_path_edit, result)
    if not success_edit:
        print(f"Failed to write modified image to {output_path_edit}")
    else:
        print(f"Modified image saved successfully to {output_path_edit}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 save_image.py <image_path>")
    else:
        save_image(sys.argv[1])
