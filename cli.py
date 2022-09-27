from rocketry import Rocketry
from rocketry.conds import (every,after_success, after_all_success)
from app.maskGenerate import mask
from app.removeBg import remove
from app.contours import createContoursFolder
from app.utils import clear, inputReady, checkImagesNum, clear_directorys
from app.folder_paths import (input_images_folder, output_without_bg_folder, output_contours_folder, output_result_mask, output_final_bg, output_final_contours, output_images_usage)

#
app = Rocketry(config={
    'task_execution': 'async',
    'task_pre_exist': 'raise',
    'force_status_from_logs': True,

    'silence_task_prerun': True,
    'silence_cond_check': True,
})

@app.task(every('30s'))
async def folder_check():
    if inputReady(input_images_folder) == True:
        pass
         
@app.task(after_success(folder_check))
async def mask_generate():
    mask(input_images_folder)
    checkImagesNum(input_images_folder,output_result_mask)

@app.task(after_success(mask_generate))
async def remove_background():
    remove(input_images_folder,output_without_bg_folder)
    checkImagesNum(input_images_folder,output_without_bg_folder)
    
@app.task(after_success(remove_background))
async def create_contours():
    createContoursFolder(output_without_bg_folder,output_contours_folder)
    checkImagesNum(input_images_folder,output_contours_folder)
    #clear('input-images/')

if __name__ == '__main__':
    app.run()