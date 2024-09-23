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
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Step 1: Define the lower and upper bounds for black in RGB
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([77, 64, 64])  # Adjust these values as needed

    # Step 2: Create a mask to extract black regions
    mask = cv2.inRange(original_image, lower_black, upper_black)

    # Create a white background
    result = np.ones_like(original_image) * 255  # White background

    # Apply the mask to retain the original colors in the foreground
    result[mask != 0] = original_image[mask != 0]

    ###########################################################
    #################### IMAGE EDITING End ####################
    ###########################################################

    output_path_edit = os.path.join(output_dir, 'processed_image.jpg')
    success_edit = cv2.imwrite(output_path_edit, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    if not success_edit:
        print(f"Failed to write modified image to {output_path_edit}")
    else:
        print(f"Modified image saved successfully to {output_path_edit}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 save_image.py <image_path>")
    else:
        save_image(sys.argv[1])
