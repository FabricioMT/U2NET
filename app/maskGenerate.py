import glob
import os
import warnings

import torch
from PIL import Image
from skimage import io
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms

from app.data_loader import RescaleT
from app.data_loader import SalObjDataset
from app.data_loader import ToTensorLab
from app.folder_paths import (input_images_folder, output_result_mask, model_in_work,execution_queue_folder)
from app.model import U2NET

warnings.simplefilter("ignore", UserWarning)

# --------- 3. model define ---------

net = U2NET(3, 1)
if torch.cuda.is_available():
    net.load_state_dict(torch.load(model_in_work))
    net.cuda()
else:
    net.load_state_dict(torch.load(model_in_work, map_location=torch.device('cpu')))


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d - mi) / (ma - mi)

    return dn

def save_output(image_name, pred, d_dir):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np * 255).convert('RGB')
    img_name = image_name.split(os.sep)[-1]
    image = io.imread(image_name)
    imo = im.resize((image.shape[1], image.shape[0]), resample=Image.LANCZOS)

    aaa = img_name.split(".")
    bbb = aaa[0:-1]
    imidx = bbb[0]
    for i in range(1, len(bbb)):
        imidx = imidx + "." + bbb[i]
    
    imo.save(r"C:\Users\fabri\OneDrive\Área de Trabalho\PyScript\U2NET\input_folder\MASK" + imidx + '.JPG')
    imo.save(d_dir + imidx + '.JPG')


def mask(input,output):
    # --------- 1. get image path and name ---------
    image_dir = os.path.join(input)
    prediction_dir = os.path.join(output)
    img_slot_0 = []
    img_name_list = glob.glob(image_dir + os.sep + '*')
    img_slot_0 = [img_name_list[0]]

    # 1. dataloader
    test_salobj_dataset = SalObjDataset(img_name_list=img_slot_0,
                                        lbl_name_list=[],
                                        transform=transforms.Compose([RescaleT(320),
                                                                      ToTensorLab(flag=0)])
                                        )
    test_salobj_dataloader = DataLoader(test_salobj_dataset,
                                        batch_size=1,
                                        shuffle=False,
                                        num_workers=1)

    net.eval()
    for i_test, data_test in enumerate(test_salobj_dataloader):

        inputs_test = data_test['image']
        inputs_test = inputs_test.type(torch.FloatTensor)

        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        # normalization
        pred = d1[:, 0, :, :]
        pred = normPRED(pred)

        save_output(img_name_list[i_test], pred, prediction_dir)

        del d1, d2, d3, d4, d5, d6, d7
