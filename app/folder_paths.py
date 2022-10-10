import os

# FOLDERS
input_images_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'input-images' + os.sep)
output_without_bg_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-removeBg' + os.sep)
output_contours_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-contours' + os.sep)
output_result_mask = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'results-mask' + os.sep)

final_output_bg = os.path.join(os.getcwd(), 'output_folder' + os.sep + 'output_removed_bg' + os.sep)
final_output_contours = os.path.join(os.getcwd(), 'output_folder' + os.sep + 'output_contours_create' + os.sep)

logs_folder = os.path.join(os.getcwd(), 'logs' + os.sep)