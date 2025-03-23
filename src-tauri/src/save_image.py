import sys
import cv2
import os
import numpy as np


sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)

def save_image(image_path):
    original_image = cv2.imread(image_path)
    if original_image is not None:
        cv2.imshow('image', original_image)
    else:
        print("The opened image is empty for some reason", file=sys.stderr)
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

    ############## EDITING ###############

    binary_mask, target_path = segment_black_text(image_path, remove_islands=True, method='connected_components', min_area=250)

    reference_images = [
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_A_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_A_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_a_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_a_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_a_typ_3_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_b_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_b_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_c_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_B_c_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_C_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_C_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_C_typ_3_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_D_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_D_typ_3_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_E_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_E_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_F_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_F_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_F_typ_3_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_F_typ_4_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_G_typ_1_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_G_typ_2_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_G_typ_3_prepared.png',
        '/home/timotej/Pictures/Stamps/Etalons/Pretisk_G_typ_4_prepared.png',
    ]

    # Detect the best match
    best_match, best_score, best_diff = detect_best_match(target_path, reference_images)
    print(f"\nBest match: {best_match}")
    print(f"Non-zero Pixels (Difference): {best_score}")

    result = best_diff

    output_path_edit = os.path.join(output_dir, 'processed_image.jpg')
    success_edit = cv2.imwrite(output_path_edit, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    if not success_edit:
        print(f"Failed to write modified image to {output_path_edit}")
    else:
        print(f"Modified image saved successfully to {output_path_edit}")

#############################################################
#################### IMAGE EDITING Start ####################
#############################################################

def load_and_preprocess(image_path):
    """Load an image, resize it to have approximately 100,000 pixels, and preprocess it to isolate the black ink."""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")

    # Calculate the current number of pixels
    height, width = image.shape[:2]
    current_pixels = height * width

    # Calculate the scaling factor to achieve approximately x pixels
    scaling_factor = np.sqrt(300000 / current_pixels)

    # Resize the image while maintaining the aspect ratio
    new_width = int(width * scaling_factor)
    new_height = int(height * scaling_factor)
    print(new_width * new_height)
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    if len(resized_image.shape) == 3 and resized_image.shape[2] == 4:  # RGBA image
        gray = cv2.cvtColor(resized_image, cv2.COLOR_RGBA2GRAY)
    else:
        return resized_image

    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    return binary

# The rest of your code remains the same...

def align_images_using_features(target, reference):
    """Align the target image to the reference image using feature-based matching."""
    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors
    kp1, des1 = sift.detectAndCompute(target, None)
    kp2, des2 = sift.detectAndCompute(reference, None)

    # Match keypoints using FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Filter good matches using Lowe's ratio test
    good_matches = [m for m, n in matches if m.distance < 0.65 * n.distance]  # Adjusted ratio

    # Ensure enough matches are found
    if len(good_matches) < 10:
        raise ValueError("Not enough good matches found for alignment.")

    # Extract location of good matches
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Compute homography matrix with RANSAC
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Check if the homography matrix is valid
    if M is None:
        raise ValueError("Homography matrix could not be computed.")

    # Warp the target image to align with the reference
    aligned = cv2.warpPerspective(target, M, (reference.shape[1], reference.shape[0]))
    return aligned, len(kp1), len(kp2), len(good_matches)

def align_images_using_template_matching(target, reference):
    """Align the target image to the reference image using template matching."""
    # Ensure the target is smaller than the reference
    if target.shape[0] > reference.shape[0] or target.shape[1] > reference.shape[1]:
        raise ValueError("Target image must be smaller than the reference image for template matching.")

    # Perform template matching
    result = cv2.matchTemplate(reference, target, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # Get the top-left corner of the matched region
    top_left = max_loc
    h, w = target.shape

    # Extract the aligned region from the reference image
    aligned = reference[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]

    return aligned

def compute_difference(aligned_target, reference):
    """Compute the difference between the aligned target and reference images and return the percentage of white pixels."""
    diff = cv2.absdiff(aligned_target, reference)
    non_zero_pixels = np.count_nonzero(diff)
    total_pixels = diff.size  # Total number of pixels in the difference image
    white_pixel_percentage = (non_zero_pixels / total_pixels) * 100  # Percentage of white pixels
    return diff, white_pixel_percentage

def detect_best_match(target_img_path, reference_images):
    """Detect the best-matching reference image for the target image."""
    target = load_and_preprocess(target_img_path)
    best_match = None
    best_score = float('inf')
    best_diff = None

    for ref_img_path in reference_images:
        try:
            reference = load_and_preprocess(ref_img_path)

            # Align target to reference using feature-based matching
            aligned_target, kp1_count, kp2_count, good_matches_count = align_images_using_features(target,
                                                                                                   reference)

            # Compute difference
            diff, non_zero_pixels = compute_difference(aligned_target, reference)

            # Print debug info
            print(f"\nReference Image: {ref_img_path}")
            # print(f"  - Keypoints in Target: {kp1_count}")
            # print(f"  - Keypoints in Reference: {kp2_count}")
            # print(f"  - Good Matches Found: {good_matches_count}")
            print(f"  - Non-zero Pixels (Difference): {non_zero_pixels}")

            # # Display the difference image in a resizable window
            # window_name = f"Difference: {ref_img_path.split('/')[-1]}"
            # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            # cv2.imshow(window_name, diff)
            # cv2.waitKey(0)  # Wait for a key press to close the window
            # cv2.destroyWindow(window_name)  # Close the window after key press

            # Update best match
            if non_zero_pixels < best_score:
                best_score = non_zero_pixels
                best_match = ref_img_path
                best_diff = diff

        except Exception as e:
            print(f"Skipping {ref_img_path} due to error: {e}")

    return best_match, best_score, best_diff

########################### GO to Preprocessing #############################

def detect_first_local_min_after_bump(hist, smooth=True, kernel_size=10):
    """
    Detect the first local minimum after the first local max in the histogram.

    Parameters:
        hist (numpy.ndarray): The histogram of the Value channel.
        smooth (bool): Whether to smooth the histogram.
        kernel_size (int): Size of the smoothing kernel.

    Returns:
        int: The index of the first local minimum after the first bump.
    """
    if smooth:
        # Smooth the histogram using a Gaussian kernel
        kernel = np.ones(kernel_size) / kernel_size
        hist = np.convolve(hist, kernel, mode='same')

    # Find the first local maximum
    bump_index = -1
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i - 1] and hist[i] > hist[i + 1] and hist[i] > 10:  # Threshold to ignore noise
            bump_index = i
            break

    if bump_index == -1:
        raise ValueError("No significant bump found in the histogram.")

    # Find the first local minimum after the bump
    min_index = -1
    for i in range(bump_index + 1, len(hist) - 1):
        if hist[i] < hist[i - 1] and hist[i] < hist[i + 1]:
            min_index = i
            break

    if min_index == -1:
        raise ValueError("No local minimum found after the bump.")

    return min_index

def remove_small_islands(mask, method='morphological', min_area=50):
    """
    Remove small islands (noise) from the binary mask.

    Parameters:
        mask (numpy.ndarray): The binary mask.
        method (str): Method to use ('morphological' or 'connected_components').
        min_area (int): Minimum area for connected components (used if method is 'connected_components').

    Returns:
        numpy.ndarray: The cleaned binary mask.
    """
    if method == 'morphological':
        # Use morphological opening to remove small islands
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  # Adjust kernel size as needed
        cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    elif method == 'connected_components':
        # Use connected component analysis to remove small islands
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        cleaned_mask = np.zeros_like(mask)
        for i in range(1, num_labels):  # Skip background (label 0)
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                cleaned_mask[labels == i] = 255
    else:
        raise ValueError("Invalid method. Choose 'morphological' or 'connected_components'.")

    return cleaned_mask

def segment_black_text(image_path, remove_islands=True, method='morphological', min_area=50):
    """
    Segment black text from an image using the HSV Value channel histogram.

    Parameters:
        image_path (str): Path to the input image.
        remove_islands (bool): Whether to remove small islands from the binary mask.
        method (str): Method to remove small islands ('morphological' or 'connected_components').
        min_area (int): Minimum area for connected components (used if method is 'connected_components').

    Returns:
        numpy.ndarray: Binary mask of the segmented black text.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]  # Extract the Value channel

    # Compute the histogram of the Value channel
    hist = cv2.calcHist([v_channel], [0], None, [256], [0, 256])
    hist = hist.flatten()

    # Detect the first local minimum after the first bump
    threshold_index = detect_first_local_min_after_bump(hist)
    threshold = threshold_index

    # Create a binary mask for the black text
    _, binary_mask = cv2.threshold(v_channel, threshold, 255, cv2.THRESH_BINARY_INV)

    # Remove small islands (noise) if requested
    if remove_islands:
        binary_mask = remove_small_islands(binary_mask, method=method, min_area=min_area)

    # Save the binary mask with the naming scheme "originalname_foreground.png"
    output_path = os.path.splitext(image_path)[0] + "_foreground.png"
    cv2.imwrite(output_path, binary_mask)
    print(f"Saved foreground mask to: {output_path}")

    return binary_mask, output_path

    ###########################################################
    #################### IMAGE EDITING End ####################
    ###########################################################

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 save_image.py <image_path>")
    else:
        print(f"Here is the sys.arv[1]: {sys.argv[1]}")
        save_image(sys.argv[1])
