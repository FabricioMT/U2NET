import os
import cv2

def resize_image(image_path, output_size):
    img = cv2.imread(image_path)
    resized_img = cv2.resize(img, output_size)
    return resized_img

def resize_images_in_folder(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.JPG') or f.endswith('.jpg') or f.endswith('.png')]
    print("!!!!",image_files)
    
    for file_name in image_files:
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        
        img = cv2.imread(input_path)
        original_height, original_width, _ = img.shape
        
        output_size = (original_width // 3, original_height // 3)
        
        resized_img = resize_image(input_path, output_size)
        
        cv2.imwrite(output_path, resized_img)

# Example usage:
input_folder = r"C:\Users\fabri\Desktop\PyScript\U2NET\input_folder\input-images/"
output_folder = r"C:\Users\fabri\Desktop\PyScript\U2NET\input_folder\testes_models\resize/"

resize_images_in_folder(input_folder, output_folder)