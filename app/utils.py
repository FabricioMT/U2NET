from logging import Filter
from rocketry.log import MinimalRecord
import os
import shutil
import time
import gdown
import torch
import pathlib as pl
from app.folder_paths import (input_images_folder,execution_queue_folder)

class SpamFilter(Filter):
    def filter(self, record: MinimalRecord) -> bool:

        start_cond = record.task_name.startswith('Start')
        finish_cond = record.task_name.startswith('Close')
        erros_cond = record.task_name.startswith('Erros')
        contours_fail = record.task_name.startswith('Create') and record.action == 'fail'
        move_cond = record.task_name.startswith('Move') and record.action == 'fail'
        bg_cond = record.task_name.startswith('RemBg') and record.action == 'fail'
        mask_cond = record.task_name.startswith('Masking') and record.action == 'fail'
        exec_cond = record.task_name.startswith('Execution') and record.action == 'fail'

        if start_cond or finish_cond or erros_cond or move_cond or contours_fail or bg_cond or mask_cond or exec_cond:
            return True
        return False

def inputReady(folder):
    inputs = os.listdir(folder)

    if len(inputs) != 0:
        return True
    else:
        raise Exception("Folder is Empty")

def clear(folder):
    for filename in os.listdir('input_folder/' + folder):
        file_path = os.path.join('input_folder/' + folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def clear_directorys():

    clear('output-removeBg/')
    clear('output-contours/')
    clear('results-mask/')

def move(inputs, output):
    srcPath = inputs
    destPath = output
    files = os.listdir(srcPath)

    for file in files[:len(files)]:
        shutil.move(srcPath + file, destPath + file)

def move_controler(inputs, output):
    output_folder = len(os.listdir(output))
    if output_folder != 0:
        move(execution_queue_folder, input_images_folder)

    move_item(inputs,output)      
    name = os.listdir(output)[0]
    packet = name
    print(packet)
    output_folder = len(os.listdir(output))
    if output_folder == 1:
        return packet
    else:
        raise Exception("Move to exec queue Error !")


def move_item(inputs,output):
    image_dir = inputs
    destPath = output
    input_img = os.listdir(image_dir)[0]
    moved_img = inputs + input_img
    shutil.move(moved_img, destPath + input_img)


def move_for_name(packet,inputs,output):
    image_dir = os.listdir(inputs)
    destPath = output
    files_image_dir = [pl.PurePath(file).name for file in image_dir]

    for filename in files_image_dir:
        if filename == packet:
            moved_img = inputs + filename
            shutil.move(moved_img, destPath + filename)



def check_dirs():
    
    if not os.path.isdir('./logs/'):
        os.makedirs('./logs/', exist_ok=True)

    if not os.path.isdir('./app/model/model_saved/'):
        os.makedirs('./app/model/model_saved/', exist_ok=True)

    if not os.path.isdir('./input_folder/'):
        os.makedirs('./input_folder/exec-queue/', exist_ok=True)
        os.makedirs('./input_folder/output-removeBg/', exist_ok=True)
        os.makedirs('./input_folder/output-contours/', exist_ok=True)
        os.makedirs('./input_folder/results-mask/', exist_ok=True)

    elif os.path.isdir('./input_folder/'):

        if not os.path.isdir('./input_folder/exec-queue/'):
            os.makedirs('./input_folder/exec-queue/', exist_ok=True)
            print("exec-queue create !")

        if not os.path.isdir('./input_folder/output-removeBg/'):
            os.makedirs('./input_folder/output-removeBg/', exist_ok=True)
            print("output-removeBg create !")

        if not os.path.isdir('./input_folder/output-contours/'):
            os.makedirs('./input_folder/output-contours/', exist_ok=True)
            print("output-contours create !")

        if not os.path.isdir('./input_folder/results-mask/'):
            os.makedirs('./input_folder/results-mask/', exist_ok=True)
            print("results-mask create !")
            
    else:
        print("Dirs Check !")

def cuda_test():
    # setting device on GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    print()
    # Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0) / 1024 ** 3, 1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0) / 1024 ** 3, 1), 'GB')

def move_for_tests():
    srcPath = r"C:\Users\fabri\Desktop\PyScript\U2NET\input_folder\testes_models\Input_Return" + os.sep
    destPath = r"C:\Users\fabri\Desktop\PyScript\U2NET\input_folder\input-images" + os.sep
    files = os.listdir(srcPath)

    for file in files[:len(files)]:
        #print(srcPath + file)
        shutil.move(srcPath + file, destPath + file)

if __name__ == "__main__":
    # remove()
    #cuda_test()
    # check_model()
    # clear('results-mask/')
    pass

