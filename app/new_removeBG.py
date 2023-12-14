import cv2
import numpy as np
from PIL import Image

def load_image_and_mask(input_folder):
  """
  Loads the input image and mask from the specified folder.

  Args:
    input_folder: Path to the folder containing the input image and mask.

  Returns:
    A tuple of the input image and mask, respectively.
  """

  input_img_path = os.path.join(input_folder, "input.jpg")
  mask_path = os.path.join(input_folder, "mask.jpg")

  # Load the input image
  input_img = cv2.imread(input_img_path)

  # Load the mask
  mask = cv2.imread(mask_path)

  # Convert the mask to grayscale
  mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

  return input_img, mask

def apply_threshold(mask_gray):
  """
  Applies a threshold to the grayscale mask.

  Args:
    mask_gray: The grayscale mask.

  Returns:
    The thresholded mask.
  """

  threshold = 0.9

  mask_thresh = mask_gray > threshold
  mask_thresh = mask_thresh.astype(np.uint8)

  return mask_thresh

def create_alpha_layer(mask_thresh):
  """
  Creates an alpha layer from the thresholded mask.

  Args:
    mask_thresh: The thresholded mask.

  Returns:
    The alpha layer.
  """

  shape = mask_thresh.shape

  alpha_layer = np.ones((shape[0], shape[1], 1), dtype=np.uint8)
  alpha_layer = alpha_layer * mask_thresh

  return alpha_layer

def combine_images(input_img, alpha_layer):
  """
  Combines the input image and alpha layer.

  Args:
    input_img: The input image.
    alpha_layer: The alpha layer.

  Returns:
    The combined image.
  """

  combined_img = np.concatenate((input_img, alpha_layer), axis=2)

  return combined_img

def remove_background(combined_img, mask_thresh):
  """
  Removes the background from the combined image.

  Args:
    combined_img: The combined image.
    mask_thresh: The thresholded mask.

  Returns:
    The image with the background removed.
  """

  removed_background = combined_img * mask_thresh

  return removed_background

def save_result_image(removed_background, output_folder):
  """
  Saves the result image to the specified folder.

  Args:
    removed_background: The image with the background removed.
    output_folder: The folder where the result image will be saved.
  """

  output_img_path = os.path.join(output_folder, "output.png")

  # Convert the image to RGB format
  removed_background = removed_background[:, :, :3]

  # Save the image
  Image.fromarray(removed_background).save(output_img_path)

def main():
  """
  The main function.
  """

  # Get the input and output folders
  input_folder = "input"
  output_folder = "output"

  # Remove the background from the image
  remove(input_folder, output_folder)

if __name__ == "__main__":
  main()
