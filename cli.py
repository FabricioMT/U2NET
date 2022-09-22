import os
from app.maskGenerate import mask
from app.removeBg import remove
from app.contours import createContoursFolder
from app.utils import clear, inputReady, checkImagesNum, move
from rocketry import Rocketry
from rocketry.conds import (every,after_success, after_all_success)


# FOLDERS
input_images_folder = os.path.join(os.getcwd(),'input_folder/'+ 'input-images/')
output_without_bg_folder = os.path.join(os.getcwd(),'input_folder/'+ 'output-removeBg/')
output_contours_folder = os.path.join(os.getcwd(),'input_folder/'+ 'output-contours/')
output_result_mask = os.path.join(os.getcwd(),'input_folder/'+'results-mask')

output_final_bg = os.path.join(os.getcwd(),'input_folder/'+'OUTPUT_FINAL_Bg/')
output_final_contours= os.path.join(os.getcwd(),'input_folder/'+'OUTPUT_FINAL_Contours/')
clear_folders = True
#

app = Rocketry(config={
    'task_execution': 'async',
    'task_pre_exist': 'raise',
    'force_status_from_logs': True,

    'silence_task_prerun': True,
    'silence_cond_check': True,
})

@app.task()
def folder_check():
    if inputReady(input_images_folder) == True:
        pass
         
@app.task(after_success(folder_check))
def mask_generate():
    mask(input_images_folder)
    checkImagesNum(input_images_folder,output_result_mask)

@app.task(after_success(mask_generate))
def remove_background():
    remove(input_images_folder,output_without_bg_folder)
    checkImagesNum(input_images_folder,output_without_bg_folder)
    
@app.task(after_success(remove_background))
def create_contours():
    createContoursFolder(output_without_bg_folder,output_contours_folder)
    checkImagesNum(input_images_folder,output_contours_folder)

@app.task(after_success(create_contours))
def move_to_dir():
    move(output_without_bg_folder,output_final_bg)
    move(output_contours_folder,output_final_contours)


@app.task(after_all_success(create_contours))
def clear_directorys():
    if clear_folders == True:
        clear('input-images/')
        clear('output-removeBg/')
        clear('output-contours/')
        clear('results-mask/')


if __name__ == '__main__':
    app.run()