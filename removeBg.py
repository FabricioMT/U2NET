import os
import cv2
import numpy as np
from PIL import Image as Img
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

def remove():
    image_dir = os.path.join(os.getcwd(), 'input-images')

    bg_dir = 'output-removeBg' + os.sep

    names = [name[:-4] for name in os.listdir(image_dir)]
    THRESHOLD = 0.9
    RESCALE = 255

    for name in names:
    # BACKGROUND REMOVAL
        if name == '.ipynb_checkpo':
            continue
        
        output = load_img('results-mask/'+name+'.png')
        out_img = img_to_array(output)
        out_img /= RESCALE

        out_img[out_img > THRESHOLD] = 1
        out_img[out_img <= THRESHOLD] = 0

        shape = out_img.shape
        a_layer_init = np.ones(shape = (shape[0],shape[1],1))
        mul_layer = np.expand_dims(out_img[:,:,0],axis=2)
        a_layer = mul_layer*a_layer_init
        rgba_out = np.append(out_img,a_layer,axis=2)

        input = load_img('input-images/'+name+'.png')
        inp_img = img_to_array(input)
        inp_img /= RESCALE

        a_layer = np.ones(shape = (shape[0],shape[1],1))
        rgba_inp = np.append(inp_img,a_layer,axis=2)

        rem_back = (rgba_inp*rgba_out)
        rem_back_scaled = rem_back*RESCALE

        # OUTPUT RESULTS

        inp_img*=RESCALE
        inp_img = np.append(inp_img,RESCALE*a_layer,axis=2)
        inp_img = cv2.resize(inp_img,(int(shape[1]/3),int(shape[0]/3)))
        rem_back = cv2.resize(rem_back_scaled,(shape[1],shape[0]))
        result_img = Img.fromarray(rem_back.astype('uint8'), 'RGBA')
        result_img.save(bg_dir+f'{name}.png')

if __name__ == "__main__":
    remove()