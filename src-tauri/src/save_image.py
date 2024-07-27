import sys
import cv2
import os

def save_image(image_path):
    print("Running save_image.py")
    print("Function argument:", image_path)

    # Verify if the image file exists
    if not os.path.isfile(image_path):
        print(f"Image file does not exist: {image_path}")
        return

    original_image = cv2.imread(image_path)
    if original_image is None:
        print("Original image is None. Please check the path or the image file.")
        return

    # Verify if the output directory exists
    output_dir = '../frontend'
    if not os.path.exists(output_dir):
        output_dir = './frontend'
        if not os.path.exists(output_dir):
            print(f"Output directory does not exist, creating: {output_dir}")
            os.makedirs(output_dir)
    output_path_orig = os.path.join(output_dir, 'orig_image.jpg')
    success_orig = cv2.imwrite(output_path_orig, original_image)
    if not success_orig:
        print(f"Failed to write original image to {output_path_orig}")
    else:
        print(f"Original image saved successfully to {output_path_orig}")

    flipped_image = cv2.flip(original_image, 1)
    output_path_edit = os.path.join(output_dir, 'processed_image.jpg')
    success_edit = cv2.imwrite(output_path_edit, flipped_image)
    if not success_edit:
        print(f"Failed to write modified image to {output_path_edit}")
    else:
        print(f"Modified image saved successfully to {output_path_edit}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 save_image.py <image_path>")
    else:
        save_image(sys.argv[1])
