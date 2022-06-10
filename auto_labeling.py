import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage .segmentation import active_contour
from skimage import measure





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
	if sc - sc_last > 0:                                    #---switch color ON
		cv2.setTrackbarPos(switch_thresh, title_window, 0)  #---turn OFF thresh
		st = 0                                              #---turn OFF thresh
	if st - st_last > 0:                                    #---switch thresh ON
		cv2.setTrackbarPos(switch_color, title_window, 0)   #---turn OFF color
		sc = 0                                              #---turn OFF color
	return sc, st

def findGeoCenter():
	for contour in contours:
		M = cv2.moments(contour)  
		centerX = int(M["m10"] / M["m00"])
		centerY = int(M["m01"] / M["m00"])
#		cv2.circle(img, (cX, cY), 5, (1, 227, 254), -1) #--- plot a filled circle at the center
		return centerX, centerY

def findSnakes():
	snakes=[]
	for contour in contours:
		((x, y), radius) = cv2.minEnclosingCircle(contour)
		scaling_factor=1.2
		radius=radius*scaling_factor
#		cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2) #--- plot minEnclosingCircle
		angle = np.linspace(0, 2*np.pi, 400)
		row = y + radius*np.sin(angle)
		column = x + radius*np.cos(angle)
		init = np.array([row, column]).T
		snake = active_contour(img_thresh, init, alpha=0.015, beta=10, gamma=0.001)
		snakes.append(snake)
		return snakes


def checkSwitchRelative():
	sr = cv2.getTrackbarPos(switch_relative, title_window)
	return sr

def applyThresh(image_input):
	if(checkSwitchRelative()):
		thresh_rel = cv2.getTrackbarPos(trackbar_thresh_rel, title_window)
		ret, img_thresh = cv2.threshold(image_input, int(float(thresh_rel/1000.0)*brightest_pixel), 255, cv2.THRESH_BINARY)
		image_threshEnabled = img_thresh
	else:			
		thresh_abs = cv2.getTrackbarPos(trackbar_thresh_abs, title_window)
		thresh_rel_check = int(float(thresh_abs/brightest_pixel)*1000)
		cv2.setTrackbarPos(trackbar_thresh_rel, title_window, thresh_rel_check)
		thresh_rel = thresh_rel_check
		ret, img_thresh = cv2.threshold(image_input, thresh_abs, 255, cv2.THRESH_BINARY)
		image_threshEnabled = img_thresh
	return image_threshEnabled



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

while(1):
	img_shown = img.copy()
	thresh_abs = cv2.getTrackbarPos(trackbar_thresh_abs, title_window)
	ret, img_thresh = cv2.threshold(img_gray, thresh_abs, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	sc_last = sc
	st_last = st
	sc, st = updateSwitchValues(sc_last, st_last)
	if st == 1: #---threshold ON
		img_shown = applyThresh(img_gray) #---apply theshold binarization for img_gray
	else:
		if sc == 1: #---color ON, threshold OFF
			img_shown = cv2.applyColorMap(img_gray, cv2.COLORMAP_JET) #---apply color map for img_gray
			cv2.drawContours(img_shown, contours, -1, (0, 0, 0), 2)   #---plot contours on img_shown 
		else:       #---color OFF, threshold OFF -> original image
			cv2.drawContours(img_shown, contours, -1, (0, 255, 0), 2) #---plot contours on img_shown
		
		
		
	cv2.imshow(title_window, img_shown)
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
#for snake in snakes:
#	ax.plot(snake[:,1], snake[:,0], 'cyan', lw=2) 
#ax.plot(snakes[:,1], snakes[:,0], 'cyan', lw=2)
plt.show()
#plt.imshow(img)