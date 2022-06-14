#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import  QWidget, QApplication, QDialog, \
	QFileDialog, QGridLayout, QLabel, QPushButton, QSlider, QComboBox
from PyQt5.QtCore import Qt
import time
import numpy as np

class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		# self.showImage()

	def initUI(self):
		self.setWindowTitle('Contours')
		self.setGeometry(100, 100, 1280, 720)
		layout = QGridLayout(self)
#		self.resize(800, 600)
		self.label = QLabel()
		self.label2 = QLabel()
		self.mycombobox = QComboBox(self)
		self.mycombobox.addItems(['Original', 'Blur', 'Colormap', 'Thresh'])
		self.mycombobox.currentIndexChanged.connect(self.onComboBoxSelected)
		self.btnOpen = QPushButton('Open Image', self)
		self.btnContours = QPushButton('Contours', self)
		self.btnContours.setEnabled(False)
		self.btnSave = QPushButton('Save Image', self)
		self.btnSave.setEnabled(False)
		self.slider = QSlider()
		self.slider.setOrientation(Qt.Horizontal)
		self.slider.setTickPosition(QSlider.TicksBelow)
		self.slider.setTickInterval(10)
		self.slider.setMinimum(0)
		self.slider.setMaximum(255)
		self.slider.valueChanged.connect(self.changed_slider)
		self.slider.setEnabled(False)	
		
		layout.addWidget(self.label, 0, 0, 4, 4)
		layout.addWidget(self.btnOpen, 4, 0, 1, 1)
		layout.addWidget(self.mycombobox, 4, 1, 1, 1)
		layout.addWidget(self.btnContours, 4, 2, 1, 1)
		layout.addWidget(self.btnSave, 4, 3, 1, 1)
		layout.addWidget(self.slider, 5, 0, 1, 2)
		layout.addWidget(self.label2)
	#	layout.addWidget(self.slider2, 5, 2, 1, 2)       		
		self.btnOpen.clicked.connect(self.openSlot)
		self.btnContours.clicked.connect(self.ContourSlot)
		self.btnSave.clicked.connect(self.saveSlot)
	#	self.slider.setValue(default_threshold)
	#	

	def openSlot(self):	
		filename, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')
		if filename == '':
			return
		self.img = cv2.imread(filename)
		if self.img.size == 1:
			return
		width = int(self.img.shape[1] * scale_percent / 100)
		height = int(self.img.shape[0] * scale_percent / 100)
		dim = (width, height)
	#	self.img = cv2.resize(self.img, dim)
		self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.brightest_pixel = np.max(self.img_gray)
		self.darkest_pixel = np.min(self.img_gray)
		self.img_blur = cv2.blur(self.img, (7, 7))
		self.img_color = cv2.applyColorMap(self.img_gray, cv2.COLORMAP_JET)
		_, self.img_thresh = cv2.threshold(self.img_gray, 90, 255, cv2.THRESH_BINARY)
		self.onComboBoxSelected()
		self.btnSave.setEnabled(True)
		self.btnContours.setEnabled(True)
		self.btnContours.setCheckable(True)
		self.slider.setEnabled(True)

	def onComboBoxSelected(self):
		if self.mycombobox.currentText() == "Original":
			self.img_shown = self.img
		elif self.mycombobox.currentText() == "Blur":
			self.img_shown = self.img_blur
		elif self.mycombobox.currentText() == "Colormap":
			self.img_shown = self.img_color
		elif self.mycombobox.currentText() == "Thresh":
			self.img_shown = cv2.cvtColor(self.img_thresh, cv2.COLOR_GRAY2RGB)
		self.img_current = self.img_shown.copy()
		self.ContourSlot()

	def ContourSlot(self):
		'''Funtions that control the contours plotting button'''
		self.img_shown = self.img_current.copy()
		if self.btnContours.isChecked():
			contours, _ = cv2.findContours(self.img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			# setting background color to light-blue
			cv2.drawContours(self.img_shown, contours, -1, (0, 0, 255), 2)
		else:
			# set background color back to light-grey
			self.btnContours.setStyleSheet("background-color : lightgrey")
			# original image
			self.img_shown = self.img_current
		self.showImage()

	def changed_slider(self):
		self.thresh = self.slider.value()
		_, self.img_thresh = cv2.threshold(self.img_gray, self.thresh, 255, cv2.THRESH_BINARY)
		thresh_in_percent = int(float(self.thresh/self.brightest_pixel)*100)
		self.onComboBoxSelected()
		self.ContourSlot()
		self.label2.setText("Threshold: {} ({}%)".format( str(self.slider.value()), str(thresh_in_percent)))

	def getslidervalue(self):
		self.ui.label.setText(f"{self.ui.horizontalSlider.value()}")
		print(self.ui.horizontalSlider.value())

	def showImage(self):
		if len(self.img_shown.shape) < 3:
			height, width = self.img_shown.shape
			bytesPerline = 1 * width
			self.qImg = QImage(self.img_shown.data, width, height, bytesPerline, QImage.Format_Grayscale8)
		else:			 
			height, width, channel = self.img_shown.shape
			bytesPerline = 3 * width
			print(height, width, channel)
			self.qImg = QImage(self.img_shown.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()	
		self.label.setPixmap(QPixmap.fromImage(self.qImg))

	def saveSlot(self):
		filename, _ = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
		if filename == '':
			return
		cv2.imwrite(filename, self.img)

if __name__ == '__main__':
	default_threshold = 90
	scale_percent = 100 # percent of original size
	start = time.time()
	App = QApplication(sys.argv)
	end = time.time()
	window = Window()
	window.show()
	sys.exit(App.exec_())