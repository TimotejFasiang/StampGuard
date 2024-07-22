import sys
import cv2

if __name__ == "__main__":
    print("Running save_image.py")
    image_path = sys.argv[1]
    original_image = cv2.imread(image_path)
    flipped_image = cv2.flip(original_image, 1)

    output_path = './frontend/orig_image.jpg'
    cv2.imwrite(output_path, original_image)

    output_path = './frontend/processed_image.jpg'
    cv2.imwrite(output_path, flipped_image)