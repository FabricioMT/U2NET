from distutils.command.config import config
from importlib.resources import path
from maskGenerate import mask
from removeBg import remove
from contours import createContoursFolder
from utils import clear, inputReady, checkImagesNum

from rocketry import Rocketry
from rocketry.conds import (after_success, after_all_success)

app = Rocketry(config={
    'task_execution': 'main',
    'task_pre_exist': 'raise',
    'force_status_from_logs': True,

    'silence_task_prerun': True,
    'silence_cond_check': True,
})

@app.task('every 1m')
def folder_check():
    print('Folder Check')
    if inputReady() == True:
        print("Start !")
         
@app.task(after_success(folder_check))
def mask_generate():
    print("Masking Init !")
    mask()
    checkImagesNum('results-mask')
    print("Masking Finished !")

@app.task(after_success(mask_generate))
def remove_background():
    print("Remove Background Init !")
    remove()
    checkImagesNum('output-removeBg')
    print("Remove Background Finished !")
    
@app.task(after_success(remove_background))
def create_contours():
    print("Contour Create Init !")
    createContoursFolder()
    checkImagesNum('output-contours')
    print("Contour Create Finished !")

@app.task(after_all_success(create_contours))
def clear_directorys():
    #clear('results-mask/')
    #clear('output-removeBg/')
    #clear('output-contours/')
    print("clear")

if __name__ == '__main__':
    app.run()