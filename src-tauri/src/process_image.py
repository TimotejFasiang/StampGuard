import sys
import cv2

if __name__ == "__main__":
    image_path = sys.argv[1]
    original_image = cv2.imread(image_path)
    flipped_image = cv2.flip(original_image, 1)
    output_path = '/home/timotej/PycharmProjects/StampGuard/src-tauri/frontend/processed_image.jpg'
    cv2.imwrite(output_path, flipped_image)

