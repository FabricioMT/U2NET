import glob
import os
import warnings

import torch
from PIL import Image
from skimage import io
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
import cv2
from app.data_loader import RescaleT
from app.data_loader import SalObjDataset
from app.data_loader import ToTensorLab
from app.folder_paths import model_in_work
from app.model import *
from typing import Any, Dict, List
import pathlib as pl
import torch.nn.functional as F
from torchvision.transforms.functional import normalize

warnings.simplefilter("ignore", UserWarning)
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
# --------- 3. model define ---------
sam_checkpoint = os.path.join(os.getcwd(), 'app', 'model', 'model_saved','others','sam_vit_h_4b8939.pth')

model_type = "vit_h"
device = "cpu"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=1,
    pred_iou_thresh=0.98,
    stability_score_thresh=0.98,
    crop_n_layers=1,
    crop_n_points_downscale_factor=1,
    min_mask_region_area=10000,  # Requires open-cv to run post-processing
    output_mode= "binary_mask"
)
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
    
    #imo.save(r"C:\Users\fabri\OneDrive\Área de Trabalho\PyScript\U2NET\input_folder\MASK" + imidx + '.JPG')
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

def Write_masks_to_folder(masks: List[Dict[str, Any]], path: str, input_path: str) -> None:
    files = os.path.join(input_path + os.sep)
    print(files)
    name = pl.PurePath(files).name.split('.')
    print(name)
    maior_area = sorted(masks, key=(lambda mask_data: mask_data['area']), reverse=True)
    if maior_area[0]:
        mask = maior_area[0]["segmentation"]
        filename = name[0]+'.JPG'
        cv2.imwrite(os.path.join(path, filename), mask * 255)
        cv2.imwrite(os.path.join(r"C:\Users\fabri\Desktop\PyScript\U2NET\input_folder/", filename), mask * 255)

def SAM_process_images(input_dir, output_mask_dir):

    img_name_list = glob.glob(input_dir + os.sep + '*')
    #print(img_name_list)

    if img_name_list[0].lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_dir, img_name_list[0])
        print("In SAM",img_path)
        # Load image
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Generate masks
        masks = mask_generator.generate(image)
        # Save the largest mask
        Write_masks_to_folder(masks, output_mask_dir, img_path)

def DIS_process_images(input_dir,result_path,model_DIS):
    input_size=[1024,1024]
    net=ISNetDIS()
    if torch.cuda.is_available():
        net.load_state_dict(torch.load(model_DIS))
        net=net.cuda()
    else:
        net.load_state_dict(torch.load(model_DIS,map_location="cpu"))
        
    print("!! DIS")
    net.eval()
    with torch.no_grad():
        img_name_list = glob.glob(input_dir + os.sep + '*')
        #print(img_name_list)

        if img_name_list[0].lower().endswith(('.jpg', '.jpeg', '.png','.JPG')):
            img_path = os.path.join(input_dir, img_name_list[0])
            print("im_path: ", img_path)
            im = io.imread(img_path)
            if len(im.shape) < 3:
                im = im[:, :, np.newaxis]
            im_shp=im.shape[0:2]
            im_tensor = torch.tensor(im, dtype=torch.float32).permute(2,0,1)
            im_tensor = F.upsample(torch.unsqueeze(im_tensor,0), input_size, mode="bilinear").type(torch.uint8)
            image = torch.divide(im_tensor,255.0)
            image = normalize(image,[0.5,0.5,0.5],[1.0,1.0,1.0])

            if torch.cuda.is_available():
                image=image.cuda()
            result=net(image)
            result=torch.squeeze(F.upsample(result[0][0],im_shp,mode='bilinear'),0)
            ma = torch.max(result)
            mi = torch.min(result)
            result = (result-mi)/(ma-mi)
            im_name= img_path.split('/')[-1].split('.')[0]
            save_output(img_path,result,result_path)
