import sys
import cv2
import os


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

    # IMAGE EDITING
    flipped_image = cv2.flip(original_image, 1)
    # IMAGE EDITING

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
