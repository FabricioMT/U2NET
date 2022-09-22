from app.maskGenerate import mask
from app.removeBg import remove
from app.contours import createContoursFolder
from app.utils import clear, inputReady, checkImagesNum
import os
from rocketry import Rocketry
from rocketry.conds import (after_success, after_all_success)


# FOLDERS
input_images_folder = os.path.join(os.getcwd(),'input_folder/'+ 'input-images/')
output_without_bg_folder = os.path.join(os.getcwd(),'input_folder/'+ 'output-removeBg')
output_contours_folder = os.path.join(os.getcwd(),'input_folder/'+ 'output-contours')
output_result_mask = os.path.join(os.getcwd(),'input_folder/'+'results-mask')
clear_folders = True
#

app = Rocketry(config={
    'task_execution': 'async',
    'task_pre_exist': 'raise',
    'force_status_from_logs': True,

    'silence_task_prerun': True,
    'silence_cond_check': True,
})

@app.task('every 1m')
def folder_check():
    print('Folder Check')
    print(input_images_folder)
    if inputReady(input_images_folder) == True:
        print("Start !")
         
@app.task(after_success(folder_check))
def mask_generate():
    print("Masking Init !")

    mask(input_images_folder)
    checkImagesNum(input_images_folder,output_result_mask)

    print("Masking Finished !")

@app.task(after_success(mask_generate))
def remove_background():
    print("Remove Background Init !")

    remove(input_images_folder,output_without_bg_folder)
    checkImagesNum(input_images_folder,output_without_bg_folder)

    print("Remove Background Finished !")
    
@app.task(after_success(remove_background))
def create_contours():
    print("Contour Create Init !")

    createContoursFolder(output_without_bg_folder,output_contours_folder)
    checkImagesNum(input_images_folder,output_contours_folder)

    print("Contour Create Finished !")

@app.task(after_all_success(create_contours))
def clear_directorys():
    if clear_folders == True:
        clear('results-mask/')
        clear('output-removeBg/')
        clear('output-contours/')
        print("Clear Folders !")

if __name__ == '__main__':
    app.run()