from distutils.command.config import config
from importlib.resources import path
from maskGenerate import mask
from removeBg import remove
from contours import createContoursFolder
from utils import clear, inputReady, checkImagesNum

from rocketry import Rocketry
from rocketry.conds import (after_success, after_all_success)

# FOLDERS

input_images_folder = 'input-images'
output_without_bg_folder = 'output-removeBg'
output_contours_folder = 'output-contours'
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
    if inputReady(input_images_folder) == True:
        print("Start !")
         
@app.task(after_success(folder_check))
def mask_generate():
    print("Masking Init !")
    mask(input_images_folder)
    checkImagesNum(input_images_folder,'results-mask')
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
    clear('results-mask/')
    clear('output-removeBg/')
    clear('output-contours/')
    print("clear")

if __name__ == '__main__':
    app.run()