import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage .segmentation import active_contour
from skimage import measure


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


#---create one initial enclosing circle for avtive contour model(snakes)
# snakes=[]
# s = np.linspace(0, 2*np.pi, 400)
# r = 100 + 105*np.sin(s)
# c = 832 + 105*np.cos(s)
# init = np.array([r, c]).T
# snakes.append(active_contour(gaussian(img_thresh, 3, preserve_range=False), init, alpha=0.015, beta=10, gamma=0.001))


#---create title window
title_window = "ICG Image"
trackbar_thresh = "Threshold"
cv2.namedWindow(title_window, cv2.WINDOW_AUTOSIZE)



def nothing(x):
    pass
#---create switch for ON/OFF functionality
switch_color = 'Color OF/OFF'
switch_thresh = 'Thresh ON/OFF'
switch_display = 'Ralative ON/OFF'
trackbar_thresh_abs = "Thresh_abs"
trackbar_thresh_rel = "Thresh_rel(‰)"
cv2.createTrackbar(switch_color, title_window, 0, 1, nothing)
cv2.createTrackbar(switch_thresh, title_window, 0, 1, nothing)
cv2.createTrackbar(switch_display, title_window, 0, 1, nothing)
thresh_abs_slider_max = 254
thresh_rel_slider_max = 1000
cv2.createTrackbar(trackbar_thresh_abs, title_window, 90, thresh_abs_slider_max, nothing)
cv2.createTrackbar(trackbar_thresh_rel, title_window, 354, thresh_rel_slider_max, nothing)
img_shown = img_gray

while(1):
#	img_shown = img_gray.copy()
	thresh_abs = cv2.getTrackbarPos(trackbar_thresh_abs, title_window)
	ret, img_thresh = cv2.threshold(img_gray, thresh_abs, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# for c in cnts:
	# 	M = cv2.moments(c)# CV2.moments會傳回一系列的moments值，我們只要知道中點X, Y的取得方式是如下進行即可。
	# 	cX = int(M["m10"] / M["m00"])
	# 	cY = int(M["m01"] / M["m00"])
	# 	cv2.circle(img, (cX, cY), 5, (1, 227, 254), -1) # 在中心點畫上黃色實心圓
	# 	((x, y), radius) = cv2.minEnclosingCircle(c)
	# 	scaling_factor=1.2
	# 	radius=radius*scaling_factor
	# 	cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2) # 畫擬合的圓，半徑放大1.2倍
	# 	s = np.linspace(0, 2*np.pi, 400)
	# 	r = y + radius*np.sin(s)
	# 	c = x + radius*np.cos(s)
	# 	init = np.array([r, c]).T
	#	snakes.append(active_contour(gaussian(img_thresh, 3, preserve_range=False), init, alpha=0.015, beta=10, gamma=0.001))
	#	print(snakes)


	# get current positions of four trackbars
	sc = cv2.getTrackbarPos(switch_color, title_window)
	st = cv2.getTrackbarPos(switch_thresh, title_window)
	sd = cv2.getTrackbarPos(switch_display, title_window)
#	print(sc, st, sd)


	if sc == 0: #color is disabled
#		print("st=", st)
		if st == 0: #threshold is disabled
			thresh_abs = cv2.getTrackbarPos(trackbar_thresh_abs, title_window)
#			print("thresh_abs=",thresh_abs)
			img_shown=img_gray.copy()
			cv2.drawContours(img_shown, contours, -1, (255, 0, 0), 2) # 畫出findContours的結果
		else:
			if sd == 0:
				thresh_abs = cv2.getTrackbarPos(trackbar_thresh_abs, title_window)
				thresh_rel_check = int(float(thresh_abs/brightest_pixel)*1000)
				cv2.setTrackbarPos(trackbar_thresh_rel, title_window, thresh_rel_check)
				thresh_rel = thresh_rel_check
				ret, img_thresh = cv2.threshold(img_gray-2, thresh_abs, 255, cv2.THRESH_BINARY)
				img_shown = img_thresh
			else:
				thresh_rel = cv2.getTrackbarPos(trackbar_thresh_rel, title_window)
				ret, img_thresh = cv2.threshold(img_gray-2, int(float(thresh_rel/1000.0)*brightest_pixel), 255, cv2.THRESH_BINARY)
				img_shown = img_thresh
	else: #---color is enabled
		cv2.setTrackbarPos(switch_thresh, title_window, 0)
		cv2.setTrackbarPos(switch_display, title_window, 0)
		img_shown = cv2.applyColorMap(img_gray, cv2.COLORMAP_JET)
		cv2.drawContours(img_shown, contours, -1, (255, 0, 0), 2) # 畫出findContours的結果

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