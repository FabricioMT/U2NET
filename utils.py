from asyncore import ExitNow
import os, shutil, torch

def clear(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def inputReady():
    input = os.listdir('input-images')
    if len(input) != 0:
        return True
    else:
        raise Exception()

def checkImagesNum(folder):
    if inputReady() == True:
        input = os.listdir('input-images')
        check = os.listdir(folder)
        if len(check) != len(input):
            raise Exception()
    else:
        raise Exception()


def cuda_test():
    # setting device on GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    print()

    #Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')

if __name__ == "__main__":
    pass
    #cuda_test()
    #clear('results-mask/')