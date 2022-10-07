from rocketry import Rocketry
from rocketry.conds import (every, after_success, after_any_fail)

from app.contours import createContoursFolder
from app.folder_paths import (input_images_folder, output_without_bg_folder, output_contours_folder)
from app.maskGenerate import mask
from app.removeBg import remove
from app.utils import inputReady, clear_directorys, delete

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
        clear_directorys()


@app.task(after_success(folder_check))
async def mask_generate():
    try:
        mask()
    except Exception:
        raise Exception("Mask Fail")


@app.task(after_success(mask_generate))
async def remove_background():
    try:
        remove(input_images_folder, output_without_bg_folder)
    except Exception:
        raise Exception("Remove Background Fail")


@app.task(after_success(remove_background))
async def create_contours():
    try:
        createContoursFolder(output_without_bg_folder, output_contours_folder)
    except Exception:
        raise Exception("Create Contour Fail")


@app.task(after_success(create_contours))
async def move_to_slab():
    try:
        # move(final_output_bg)
        # move(final_output_contours)
        delete(input_images_folder)
    except Exception:
        raise Exception("Move Finish Fail")


@app.task(after_any_fail(mask_generate, remove_background, create_contours))
async def clear_for_erro():
    clear_directorys()


if __name__ == '__main__':
    app.run()
