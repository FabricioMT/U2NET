import os, shutil, torch, gdown
from PIL import Image, ExifTags

def inputReady(folder):
    input = os.listdir(folder)
    if len(input) != 0:
        return True
    else:
        raise Exception("Folder is Empity !")

def clear(folder):
    for filename in os.listdir('input_folder/'+ folder):
        file_path = os.path.join('input_folder/'+ folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def checkImagesNum(input_folder,check_folder):
    if inputReady(input_folder) == True:
        input = os.listdir(input_folder)
        check = os.listdir(check_folder)
        if len(check) != len(input):
        
            raise Exception("Folder go clear !")
    else:
        raise Exception("Folder is Empity !")

def move(input,output):

    srcPath = input
    destPath = output
    files = os.listdir(srcPath)

    for file in files[:len(files)]:
        shutil.move(srcPath + file, destPath + file)

def check_model():
    if os.path.isdir('./app/model/model_saved/') == False:
        os.makedirs('./app/model/model_saved/', exist_ok=True)
        gdown.download('https://drive.google.com/file/d/1BZWoNTdO8JRA3S9bwKncVD5KXQbq-5sB/view?usp=sharing',
        './app/model/model_saved/u2net.pth',
        quiet=False)
    else:
        print("Model OK !")



def extract_metadata(folder):
    img = os.listdir(folder)
    img = Image.open("/path/to/file.jpg")
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    print(exif)

def clear_directorys():
    #clear('input-images/')
    clear('output-removeBg/')
    clear('output-contours/')
    clear('results-mask/')

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
    #check_model()
    #clear('results-mask/')