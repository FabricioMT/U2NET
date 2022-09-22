import os, cv2
import numpy as np

def createContours(img):
	image = cv2.imread(img, cv2.IMREAD_UNCHANGED)
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret, image_edges = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)
	mask = np.zeros(image_gray.shape, np.float32)
	mask.fill(255)

	contours, hierarchyct = cv2.findContours(image=image_edges,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
	#thickness=-1
	cv2.drawContours(image=mask,contours=contours,contourIdx=-1,color=(0,0,0),thickness=1)
	return mask

def createContoursFolder(input_rembg_folder,output_cont):
	image_dir = os.path.join(os.getcwd(), input_rembg_folder)
	image_dest = os.path.join(os.getcwd(), output_cont + os.sep)
	files = os.listdir(image_dir)

	n = 0
	finish = len(files)

	for file in files:
		contour = createContours(image_dir + os.sep + file)

		if cv2.imwrite(image_dest + file, contour):
			print("Image Contour Create in :",image_dest + file)
		else:
			print("Create Image Error !")
			return 1

		n = n+1
		if n == finish: 
			print('Finish !')
			return 0

if __name__ == "__main__":
    createContoursFolder()