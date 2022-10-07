import gdown
import os
import shutil
import torch


def inputReady(folder):
    input_folder = os.listdir(folder)
    if len(input_folder) == 0:
        raise Exception("Folder is Empty !")
    else:
        return True


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


def delete(input_folder):
    image_dir = input_folder
    input_img = os.listdir(image_dir)[0]
    removed_img = input_folder + input_img
    os.remove(removed_img)


def move(input_folder, output):
    srcPath = input_folder
    destPath = output
    files = os.listdir(srcPath)

    for file in files[:len(files)]:
        shutil.move(srcPath + file, destPath + file)


def check_model():
    if not os.path.isdir('./app/model/model_saved/'):
        print("Donwload Model !")
        os.makedirs('./app/model/model_saved/', exist_ok=True)
        gdown.download('https://drive.google.com/file/d/1RWApr3ItjWVPgBL75Tm1_fv3dfy3mBrv/view?usp=sharing',
                       './app/model/model_saved/u2net.pth',
                       quiet=False)
    else:
        print("Model OK !")


def clear_directorys():
    # clear('input-images/')
    clear('output-removeBg/')
    clear('output-contours/')
    clear('results-mask/')


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


if __name__ == "__main__":
    pass
    # cuda_test()
    # check_model()
    # clear('results-mask/')
