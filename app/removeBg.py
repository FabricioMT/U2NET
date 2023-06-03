import os

import cv2
import numpy as np
from PIL import Image as Img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img

from app.folder_paths import (output_result_mask)
from app.utils import clear


def remove(input_folder, output_folder):
    image_dir = os.path.join(os.getcwd(), input_folder)
    bg_dir = os.path.join(os.getcwd(), output_folder + os.sep)


    input_img = os.listdir(image_dir)[0]
    file = os.listdir(output_result_mask)[0]
    img_name = input_img[:-4]
    THRESHOLD = 0.9
    RESCALE = 255

    mask = cv2.imread(output_result_mask + file)
    image_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    out_img = img_to_array(image_gray)
    out_img /= RESCALE
    out_img[out_img > THRESHOLD] = 1
    out_img[out_img <= THRESHOLD] = 0

    shape = out_img.shape
    a_layer_init = np.ones(shape=(shape[0], shape[1], 0))
    mul_layer = np.expand_dims(out_img[:, :, 0], axis=2)
    a_layer = mul_layer * a_layer_init
    rgba_out = np.append(out_img, a_layer, axis=2)

    input = load_img(image_dir + input_img)
    inp_img = img_to_array(input)
    inp_img /= RESCALE

    a_layer = np.ones(shape=(shape[0], shape[1], 1))
    rgba_inp = np.append(inp_img, a_layer, axis=2)

    rem_back = (rgba_inp * rgba_out)
    rem_back_scaled = rem_back * RESCALE

    # OUTPUT RESULTS

    inp_img *= RESCALE
    inp_img = np.append(inp_img, RESCALE * a_layer, axis=2)
    #inp_img = cv2.resize(inp_img, (int(shape[1] / 3), int(shape[0] / 3)))
    rem_back = cv2.resize(rem_back_scaled, (shape[1], shape[0]))
    result_img = Img.fromarray(rem_back.astype('uint8'), 'RGBA')
    result_img.save(bg_dir + f'{img_name}.png')
    clear('results-mask/')

    
