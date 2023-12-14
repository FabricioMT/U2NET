import logging

from rocketry import Rocketry
from rocketry.conds import (after_any_success, after_success, after_any_fail, after_fail,after_finish)
from rocketry.log import TaskLogRecord
from redbird.repos import CSVFileRepo
from redbird.logging import RepoHandler

from rocketry.args import Return
from app.contours import createContoursFolder
from app.crop import cropBoundingBoxFolder

from app.folder_paths import (input_images_folder, 
                              output_without_bg_folder, 
                              output_contours_folder, 
                              logs_folder,
                              final_output_bg, 
                              final_output_contours, 
                              final_input,
                              execution_queue_folder,
                              output_crop_no_background_Box,
                              output_result_mask,
                              final_output_crop,
                              output_crop)

from app.maskGenerate import mask
from app.removeBg import remove
from app.utils import (inputReady, clear_directorys, move_item,SpamFilter, move,move_for_tests,move_controler,move_for_name,check_dirs)

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
#logger.addHandler(logging.StreamHandler())
logger.addHandler(folder)

@app.task(on_startup=True, name='Start')
def Start():
    check_dirs()
    print("Start")
    relax = input("Informe o valor de sobra para o Crop: ")

    return relax


@app.task(on_shutdown=True,name='Close')
def Close():
    print("Close")
    #move_for_tests()
    move(execution_queue_folder, input_images_folder)
    clear_directorys()
    pass


@app.task(after_fail('Folder Check'))
def Restart():
    #print("Restart")
    pass

@app.task(after_success('Move to Slab'))
def Next():
    print("Open Next File !")
    pass


@app.task(after_any_success(Start,Restart,Next),name='Folder Check')
def folder_check():
    #print("foldercheck")
    if inputReady(input_images_folder):
        clear_directorys()

@app.task(after_success('Folder Check'),name='Execution')
def execution_queue():
    print("Execution")
    try:
        packet = move_controler(input_images_folder,execution_queue_folder)
        if len(execution_queue_folder) == 1:
            raise Exception("execution_queue Fail !")
    except Exception:
        raise Exception("execution_queue Fail !")
    return packet


@app.task(after_success('Execution'), name='Masking')
def mask_generate():
    #print("Masking")
    try:
        mask(execution_queue_folder,output_result_mask)
    except Exception:
        raise Exception("Mask Fail")

@app.task(after_success(mask_generate), name='RemBg')
def remove_background():
    #print("Rembg")
    try:
        remove(execution_queue_folder, output_without_bg_folder)
    except Exception:
        raise Exception("Remove Background Fail")


@app.task(after_success(remove_background), name='Create Contours')
def create_contours():
    #print("createcontours")
    try:
        pass
        createContoursFolder(output_without_bg_folder, output_contours_folder)
    except Exception:
        raise Exception("Create Contour Fail")

@app.task(after_success(create_contours), name='Crop')
def crop_bounding_box(relax=Return(Start)):
    #print("Crop")
    try:
        cropBoundingBoxFolder(execution_queue_folder, 
                              output_without_bg_folder,
                              output_crop,
                              output_crop_no_background_Box,
                              relax)
    except Exception:
        raise Exception("crop_bounding_box Fail")

@app.task(after_success(crop_bounding_box), name='packet_move')
def packet_move(packet=Return(execution_queue)):
    try:
        move_for_name(packet,execution_queue_folder,final_input)
    except Exception:
        raise Exception("Move Finish Fail")
    

@app.task(after_success(packet_move), name='Move to Slab')
def move_to_slab():
    try:

        move(output_without_bg_folder,final_output_bg)
        move(output_contours_folder,final_output_contours)
        move(output_crop,final_output_crop)


    except Exception:
        raise Exception("Move Finish Fail")


@app.task(after_any_fail(mask_generate, remove_background, create_contours), name='Erros')
def clear_for_erro():
    #print("Clear")
    clear_directorys()


if __name__ == "__main__":
    app.run()