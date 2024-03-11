import os
import cv2
import numpy as np

def cropBoundingBox(image_orignal,image_png,relax_val):
    img_original = cv2.imread(image_orignal,cv2.IMREAD_UNCHANGED)
    img = cv2.imread(image_png, cv2.IMREAD_UNCHANGED)

    relax = int(relax_val)
    image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, image_edges = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pixel_count = []

    for component in contours: pixel_count.append(len(component))

    max_pixel_ct = pixel_count.index(max(pixel_count))

    x, y, w, h = cv2.boundingRect(contours[max_pixel_ct])

    cv2.rectangle(img, (x,y),(x+w,y+h), (255, 255, 255), 1)

    x_relaxed, y_relaxed, w_relaxed, h_relaxed = max(0, x-relax), max(0, y-relax), min(img.shape[1], x + w + relax), min(img.shape[0], y + h + relax)
    #print(f"Original: {x, y, w, h}, Relaxed: {x_relaxed, y_relaxed, w_relaxed, h_relaxed}")
    cv2.rectangle(img, (x_relaxed, y_relaxed), (w_relaxed, h_relaxed), (0, 255, 0), 1)
    cropped_image = img_original[max(0, y-relax):min(img.shape[0], y + h + relax), max(0, x-relax):min(img.shape[1], x + w + relax)].astype(np.uint8)
    # cv2.imshow('file_o', img_original)
    #cv2.imshow('file_wb', img)
    # cv2.imshow('cropped_image', cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped_image

def crop_no_background_Box(image_orignal,image_png,relax_val):
    img_original = cv2.imread(image_orignal,cv2.IMREAD_UNCHANGED)
    img = cv2.imread(image_png, cv2.IMREAD_UNCHANGED)

    relax = int(relax_val)
    image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, image_edges = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pixel_count = []

    for component in contours: pixel_count.append(len(component))

    max_pixel_ct = pixel_count.index(max(pixel_count))

    x, y, w, h = cv2.boundingRect(contours[max_pixel_ct])

    x_relaxed, y_relaxed, w_relaxed, h_relaxed = max(0, x-relax), max(0, y-relax), min(img.shape[1], x + w + relax), min(img.shape[0], y + h + relax)
    cropped_image = img[max(0, y-relax):min(img.shape[0], y + h + relax), max(0, x-relax):min(img.shape[1], x + w + relax)].astype(np.uint8)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped_image

def cropBoundingBoxFolder(input_orgin, without_bg, output,output_crop_no_background_Box,relax_val):
    image_origin = os.path.join(os.getcwd(), input_orgin)
    image_without_bg_folder = os.path.join(os.getcwd(), without_bg)
    image_dest = os.path.join(os.getcwd(), output)
    image_dest_2 = os.path.join(os.getcwd(), output_crop_no_background_Box)

    image_origin_files = sorted([f for f in os.listdir(image_origin) if f.endswith('.JPG') or f.endswith('.jpg') or f.endswith('.png')])
    image_without_bg_folder_files = sorted([f for f in os.listdir(image_without_bg_folder) if f.endswith('.JPG') or f.endswith('.jpg') or f.endswith('.png')])
    
    for file_o,file_wb in zip(image_origin_files,image_without_bg_folder_files):
        crop_img = cropBoundingBox(
            os.path.join(image_origin, file_o),
            os.path.join(image_without_bg_folder, file_wb),
            relax_val)
        
        crop_no_background = crop_no_background_Box(
            os.path.join(image_origin, file_o),
            os.path.join(image_without_bg_folder, file_wb),
            relax_val)


        
        if cv2.imwrite(image_dest + file_o, crop_img):
            pass
        else:
            raise

        if cv2.imwrite(image_dest_2 + f'{file_o[:-4]}.png',crop_no_background):
            pass
        else:
            raise



    

