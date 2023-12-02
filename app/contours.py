import os
import cv2
import numpy as np

def createContours(img):
    image = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image_edges = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)
    mask = np.zeros(image_gray.shape, np.float32)
    mask.fill(255)

    contours, hierarchyct = cv2.findContours(image=image_edges,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    
    pixel_count = []

    for component in contours: pixel_count.append(len(component))

    max_pixel_ct = pixel_count.index(max(pixel_count))

    cv2.drawContours(image=mask,contours=contours[max_pixel_ct],contourIdx=-1,color=(0,0,0),thickness=1)
    #thickness=-1
    return mask


def createContoursFolder(input_rembg_folder, output_cont):
    image_dir = os.path.join(os.getcwd(), input_rembg_folder)
    image_dest = os.path.join(os.getcwd(), output_cont + os.sep)
    files = os.listdir(image_dir)

    for file in files:
        contour = createContours(image_dir + os.sep + file)

        if cv2.imwrite(image_dest + file, contour):
            pass
        else:
            raise
