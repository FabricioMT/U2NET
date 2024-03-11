import logging

from rocketry import Rocketry
from rocketry.conds import (after_any_success, after_success, after_any_fail, after_fail,after_finish)
from rocketry.log import TaskLogRecord
from redbird.repos import CSVFileRepo
from redbird.logging import RepoHandler
import os
from rocketry.args import Return
from app.contours import createContoursFolder
from app.crop import cropBoundingBoxFolder

from app.folder_paths import (input_images_folder, 
                              output_without_bg_folder, 
                              output_contours_folder, 
                              logs_folder,final_output_bg, 
                              final_output_contours,
                              final_input,
                              execution_queue_folder,
                              output_result_mask,
                              output_erros,
                              final_output_crop,
                              output_crop)

from app.maskGenerate import mask,SAM_process_images,DIS_process_images
from app.removeBg import remove
from app.utils import (inputReady, clear_directorys,SpamFilter, move,move_for_tests,move_controler,move_for_name,check_dirs)

app = Rocketry(config={
    'task_execution': 'async',
    'task_pre_exist': 'raise',
    'force_status_from_logs': True,
    'silence_task_prerun': True,
    'silence_cond_check': True,
    'silence_task_logging': True,
})
model_DIS = os.path.join(os.getcwd(), 'app', 'model', 'model_saved','others','gpu_itr_14000_traLoss_0.1983_traTarLoss_0.0033_valLoss_2.753_valTarLoss_0.1347_maxF1_0.9862_mae_0.0185_time_0.028574.pth')
logger = logging.getLogger("rocketry.task")
repo = CSVFileRepo(filename= logs_folder + "log.csv", model=TaskLogRecord)
folder = RepoHandler(repo=repo)
folder.addFilter(SpamFilter())
#logger.addHandler(logging.StreamHandler())
logger.addHandler(folder)

@app.task(on_startup=True, name='Start')
def Start():
    check_dirs()
    move(execution_queue_folder, input_images_folder)
    print("start")
    relax = input("Informe o valor de sobra para o Crop: ")
    model = input("Informe o modelo: [u2net] - [sam] - [DIS]:")

    return relax,model


@app.task(on_shutdown=True,name='Close')
def Close():
    print("Close")
    move_for_tests()
    move(execution_queue_folder, input_images_folder)
    clear_directorys()
    pass


@app.task(after_fail('Folder Check'))
def Restart():
    print("Restart")
    pass

@app.task(after_success('Move to Slab'))
def Next():
    print("Open Next File !")
    pass


@app.task(after_any_success(Start,Restart,Next,'Erros'),name='Folder Check')
def folder_check():
    print("foldercheck")
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
def mask_generate(model=Return(Start)):
    print("Masking")
    try:
        if model[1] == 'u2net':
            mask(execution_queue_folder,output_result_mask)
        elif model[1] == 'sam':
            SAM_process_images(execution_queue_folder,output_result_mask)
        elif model[1] == 'DIS':
            DIS_process_images(execution_queue_folder,output_result_mask,model_DIS)

    except Exception:
        raise Exception("Mask Fail")

@app.task(after_success(mask_generate), name='RemBg')
def remove_background():
    print("Rembg")
    try:
        remove(execution_queue_folder, output_without_bg_folder)
    except Exception:
        raise Exception("Remove Background Fail")


@app.task(after_success(remove_background), name='Create Contours')
def create_contours():
    print("createcontours")
    try:
        createContoursFolder(output_without_bg_folder, output_contours_folder)
    except Exception:
        raise Exception("Create Contour Fail")

@app.task(after_success(create_contours), name='Crop')
def crop_bounding_box(relax=Return(Start)):
    print("Crop")
    try:
        cropBoundingBoxFolder(execution_queue_folder,
                              output_without_bg_folder,
                              output_crop,
                              relax[0])
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


@app.task(after_any_fail(mask_generate, remove_background, create_contours,execution_queue), name='Erros')
def clear_for_erro(packet=Return(execution_queue)):
    print("Clear")
    move_for_name(packet,execution_queue_folder,output_erros)
    clear_directorys()


if __name__ == "__main__":
    app.run()