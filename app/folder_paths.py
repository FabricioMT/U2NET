import os
model_in_work = os.path.join(r'D:\Models\Model_Saved_U2NET' + os.sep + "Grey_PosSAM_fullTransform-_0.0001_Loss_0.124252_Epoch_201.pth") # testes


# FOLDERS u2net.pthGrey_CorrectRC120_0.0001_Loss_0.080863_Epoch_101
input_images_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'input-images' + os.sep)
execution_queue_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'exec-queue' + os.sep)
output_without_bg_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-removeBg' + os.sep)
output_contours_folder = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'output-contours' + os.sep)
output_result_mask = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'results-mask' + os.sep)

# FOLDERS PASTE YOUR PATHS
final_output_bg = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + '04-12m' + os.sep)
final_output_contours = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + '04-12mm' + os.sep)
final_input = os.path.join(os.getcwd(), 'input_folder' + os.sep + 'testes_models' + os.sep + '04-12input' + os.sep)

logs_folder = os.path.join(os.getcwd(), 'logs' + os.sep)

# input_images_folder = os.path.join(r'D:\Data_set_Inits\green_data\a' + os.sep)
# final_input = os.path.join(r"D:\Data_set_Inits\NEW GREEN TEST\image" + os.sep)
# final_output_bg = os.path.join(r'D:\Data_set_Inits\NEW GREEN TEST\premask' + os.sep)

