import os

model_in_work = os.path.join(os.getcwd(), 'app' + os.sep + 'model' + os.sep+ 'model_saved' + os.sep + "Model_Version_1.2.3.pth") # testes

colectdisk = os.getcwd()
disk = colectdisk[:2]

# FOLDERS 
#input_images_folder = os.path.join(disk + os.sep + 'input_folder'  + os.sep + 'input-images' + os.sep)
input_images_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'input-images' + os.sep)
#input_images_folder = os.path.join(r'D:\Data_set_Inits\CS3\cs3_originals\Original_CS3_4k_forzip' + os.sep)
execution_queue_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'exec-queue' + os.sep)
output_without_bg_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-removeBg' + os.sep)
output_contours_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-contours' + os.sep)
output_result_mask = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'results-mask' + os.sep)
output_crop = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-crop' + os.sep)
output_crop_no_background_Box = os.path.join(os.getcwd(), 'output_geral' + os.sep + 'Output_Removed_Background_CROP' + os.sep)
# FOLDERS PASTE YOUR PATHS
final_input = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + 'Input_Return' + os.sep)
final_output_bg = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + 'Output_Removed_Background' + os.sep)
final_output_contours = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + 'Output_Edges' + os.sep)
final_output_crop = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + 'cropBoundingBox' + os.sep)
#final_output_crop = os.path.join(r'D:\Data_set_Inits\CS3\cs3_originals\crop'+ os.sep)
output_erros = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + 'Erros' + os.sep)

logs_folder = os.path.join(os.getcwd(), 'logs' + os.sep)


