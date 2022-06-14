import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage .segmentation import active_contour
from skimage import measure
import random
import time




#---create one initial enclosing circle for avtive contour model(snakes)
# snakes=[]
# s = np.linspace(0, 2*np.pi, 400)
# r = 100 + 105*np.sin(s)
# c = 832 + 105*np.cos(s)
# init = np.array([r, c]).T
# snakes.append(active_contour(gaussian(img_thresh, 3, preserve_range=False), init, alpha=0.015, beta=10, gamma=0.001))





def nothing(x):
    pass

def createGUI():
	'''Functions that create the trackbar interface'''
	cv2.createTrackbar(switch_color, title_window, 0, 1, nothing)
	cv2.createTrackbar(switch_thresh, title_window, 0, 1, nothing)
	cv2.createTrackbar(switch_relative, title_window, 0, 1, nothing)
	cv2.createTrackbar(trackbar_thresh_abs, title_window, 90, thresh_abs_slider_max, nothing)
	cv2.createTrackbar(trackbar_thresh_rel, title_window, 354, thresh_rel_slider_max, nothing)

def updateSwitchValues(sc_last, st_last):
	'''Functions that updates the Switch ON/OFF values'''
	sc = cv2.getTrackbarPos(switch_color, title_window)
	st = cv2.getTrackbarPos(switch_thresh, title_window)
	sr = cv2.getTrackbarPos(switch_relative, title_window)
	if sc - sc_last > 0:                                    #---switch color ON
		cv2.setTrackbarPos(switch_thresh, title_window, 0)  #---turn OFF thresh
		st = 0                                              #---turn OFF thresh
	if st - st_last > 0:                                    #---switch thresh ON
		cv2.setTrackbarPos(switch_color, title_window, 0)   #---turn OFF color
		sc = 0                                              #---turn OFF color
	return sc, st, sr

def findGeoCenter(input_image):
	centerX=[]
	centerY=[]
	for contour in contours:
		M = cv2.moments(contour)  
		centerX.append(int(M["m10"] / M["m00"]))
		centerY.append(int(M["m01"] / M["m00"]))
#		cv2.circle(input_image, (centerX, centerY), 5, (1, 227, 254), -1) #--- plot a filled circle at the center
	return centerX, centerY

def findSnakes(input_image):
	snakes=[]
	for contour in contours:
		((x, y), radius) = cv2.minEnclosingCircle(contour)
		scaling_factor=1.2
		radius=radius*scaling_factor
		cv2.circle(input_image, (int(x), int(y)), int(radius), (0, 255, 0), 2) #--- plot minEnclosingCircle
		angle = np.linspace(0, 2*np.pi, 400)
		row = y + radius*np.sin(angle)
		column = x + radius*np.cos(angle)
		init = np.array([row, column]).T
	#	snake = active_contour(img_thresh, init, alpha=0.015, beta=10, gamma=0.001)
	#	snakes.append(snake)
	return snakes


def applyThresh(sr, image_input):
	if sr == 1:
		t_rel = cv2.getTrackbarPos(trackbar_thresh_rel, title_window)
		t_rel2abs = int(float(t_rel/1000)*brightest_pixel)
		cv2.setTrackbarPos(trackbar_thresh_abs, title_window, t_rel2abs)
		ret, img_thresh = cv2.threshold(image_input, t_rel2abs, 255, cv2.THRESH_BINARY)
	elif sr == 0:
		t_abs = cv2.getTrackbarPos(trackbar_thresh_abs, title_window)
		t_abs2rel = int(float(t_abs/brightest_pixel)*1000)
		cv2.setTrackbarPos(trackbar_thresh_rel, title_window, t_abs2rel)
		ret, img_thresh = cv2.threshold(image_input, t_abs, 255, cv2.THRESH_BINARY)
	return img_thresh


def drawUserDefinedContours(input_image, contours_selected, color):
	cv2.drawContours(input_image, contours_selected, -1, color, 2)   #---plot contours on img_shown


def label_contours(input_image, contours_selected):
	label=1
	for contour in contours_selected:
		max_positionY = 0
		for point in contour:
			if point[0][1] > max_positionY:
				max_positionY = point[0][1]
				max_positionX = point[0][0]
		cv2.putText(input_image, str(label), (max_positionX, max_positionY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
		label+=1 

img=cv2.imread("./test_image.png")
img_ablur = cv2.blur(img, (5, 5)) #---averaging
img_gblur = cv2.GaussianBlur(img, (5, 5), 0) #---Gaussian blurring
img_mblur = cv2.medianBlur(img, 5) #---median blurring
#cv2.imwrite("./test_blur.png", ablur)
#cv2.imwrite("./test_gblur.png",gblur)
#cv2.imwrite("./test_mblur.png",mblur)
#cv2.imshow('blur',blur)
#cv2.waitKey(0)
img_gray = cv2.cvtColor(img_ablur, cv2.COLOR_BGR2GRAY)
brightest_pixel = np.max(img_gray)
print(brightest_pixel)
darkest_pixel = np.min(img_gray)

#---create title window
title_window = "ICG Image"
switch_color = 'Color OF/OFF'
switch_thresh = 'Thresh ON/OFF'
switch_relative = 'Relative ON/OFF'
trackbar_thresh_abs = "Thresh_abs"
trackbar_thresh_rel = "Thresh_rel(‰)"
thresh_abs_slider_max = 254
thresh_rel_slider_max = 1000
cv2.namedWindow(title_window, cv2.WINDOW_AUTOSIZE)
createGUI()
sc = 0
st = 0
area_thresh=10000

def f():
    for i in range(10000):
        "-".join(str(n) for n in range(100))
    time.sleep(1)


while(1):
	start = time.process_time()
	#f()	
	img_shown = img.copy()
	sc_last = sc
	st_last = st
	sc, st, sr = updateSwitchValues(sc_last, st_last)
	img_thresh = applyThresh(sr, img_gray)

	contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# centerX, centerY = findGeoCenter(img_shown)
	# snakes = findSnakes(img_shown)
	# for snake in snakes:
	# 	points = np.array(snake, np.int32)
	# 	cv2.polylines(img_shown, pts=[points], isClosed=False, color=(0, 0, 255), thickness=3)
	

	if st == 1: #---threshold ON
		img_shown = img_thresh #---apply theshold binarization for img_gray
	else:
		if sc == 1: #---color ON, threshold OFF
			img_shown = cv2.applyColorMap(img_gray, cv2.COLORMAP_JET) #---apply color map for img_gray
			color=(0, 0, 0)
			
		else:       #---color OFF, threshold OFF -> original image
			color=(0, 255, 0)
		contours_selected=[]
		for contour in contours:
			# area = cv2.contourArea(contour)  #計算面積
			# if area < area_thresh:
			# 	continue
			contours_selected.append(contour)

		drawUserDefinedContours(img_shown, contours_selected, color)
		label_contours(img_shown, contours_selected)		
	cv2.imshow(title_window, img_shown)
	end = time.process_time()	
#	print("process_time 測量時間：%f 秒" % (end - start))
#	print("FPS：%f" % float(1/(end - start)))
#	cv2.waitKey(0)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

# Wait until user press some key




fig, ax = plt.subplots(figsize=(7,7))
ax.imshow(img,cmap=plt.cm.gray)

#---plot initial enclosing circle
# ax.plot(init[:,1], init[:,0], '--r', lw=3)

#---plot active contour model results
 
#ax.plot(snakes[:,1], snakes[:,0], 'cyan', lw=2)
plt.show()
#plt.imshow(img)