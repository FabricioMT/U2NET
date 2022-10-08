import logging
import os

from rocketry import Rocketry
from rocketry.conds import (after_any_success, after_success, after_any_fail, after_fail)
from rocketry.log import TaskLogRecord

from redbird.repos import CSVFileRepo
from redbird.logging import RepoHandler

from app.contours import createContoursFolder
from app.folder_paths import (input_images_folder, output_without_bg_folder, output_contours_folder,logs_folder)
from app.maskGenerate import mask
from app.removeBg import remove
from app.utils import inputReady, clear_directorys, delete

app = Rocketry(config={
    'task_execution': 'async',
    'task_pre_exist': 'ignore',
    'force_status_from_logs': False,
    'silence_task_prerun': False,
    'silence_cond_check': True,
})

logger = logging.getLogger("rocketry.task")
logger.addHandler(logging.StreamHandler())
repo = CSVFileRepo(filename= logs_folder + "log.csv", model=TaskLogRecord)
handler = RepoHandler(repo=repo)
logger.addHandler(handler)

@app.task(on_startup=True)
def Start():
    pass


@app.task(after_fail('Folder Check'))
def Restart():
    #while len(os.listdir(input_images_folder)) == 0:
        pass


@app.task(after_any_success(Start,'Move to Slab',Restart), name='Folder Check')
def folder_check():
    if inputReady(input_images_folder):
        clear_directorys()


@app.task(after_success('Folder Check'), name='Masking')
def mask_generate():
    try:
        mask()
    except Exception:
        raise Exception("Mask Fail")


@app.task(after_success(mask_generate), name='RemBg')
def remove_background():
    try:
        remove(input_images_folder, output_without_bg_folder)
    except Exception:
        raise Exception("Remove Background Fail")


@app.task(after_success(remove_background), name='Create Contours')
def create_contours():
    try:
        createContoursFolder(output_without_bg_folder, output_contours_folder)
    except Exception:
        raise Exception("Create Contour Fail")


@app.task(after_success(create_contours), name='Move to Slab')
def move_to_slab():
    try:
        # move(final_output_bg)
        # move(final_output_contours)
        delete(input_images_folder)
    except Exception:
        raise Exception("Move Finish Fail")
    return True


@app.task(after_any_fail(mask_generate, remove_background, create_contours), name='Erros', execution='async')
async def clear_for_erro():
    clear_directorys()

if __name__ == "__main__":    
    app.run()