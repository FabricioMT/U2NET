import logging

from rocketry import Rocketry
from rocketry.conds import (after_any_success, after_success, after_any_fail, after_fail)
from rocketry.log import TaskLogRecord
from rocketry.args import Return
from redbird.repos import CSVFileRepo
from redbird.logging import RepoHandler


from app.contours import createContoursFolder
from app.folder_paths import (input_images_folder, output_without_bg_folder, output_contours_folder,logs_folder)
from app.maskGenerate import mask
from app.removeBg import remove
from app.utils import inputReady, clear_directorys, delete, SpamFilter

app = Rocketry(config={
    'task_execution': 'async',
    'task_pre_exist': 'raise',
    'force_status_from_logs': True,
    'silence_task_prerun': True,
    'silence_cond_check': True,
    'silence_task_logging': True,
})

logger = logging.getLogger("rocketry.task")
repo = CSVFileRepo(filename= logs_folder + "log.csv", model=TaskLogRecord)
folder = RepoHandler(repo=repo)
folder.addFilter(SpamFilter())
logger.addHandler(logging.StreamHandler())
logger.addHandler(folder)

sucess_count = 0
@app.task(on_startup=True, name='Start')
def Start():
    pass

@app.task(on_shutdown=True,name='Close')
def Close(count=Return('Move to Slab')):
    print('Total Contours Create: ',count)


@app.task(after_fail('Folder Check'))
def Restart():
    pass

@app.task(after_any_success(Start,'Move to Slab',Restart),name='Folder Check')
def folder_check():
    if inputReady(input_images_folder):
        clear_directorys()

#
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
    sucess_count = sucess_count + 1
    try:
        # move(final_output_bg)
        # move(final_output_contours)
        delete(input_images_folder)

    except Exception:
        raise Exception("Move Finish Fail")
    return sucess_count


@app.task(after_any_fail(mask_generate, remove_background, create_contours), name='Erros')
async def clear_for_erro():
    clear_directorys()


if __name__ == "__main__":  

    app.run()