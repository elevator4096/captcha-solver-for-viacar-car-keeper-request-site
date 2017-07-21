import numpy as np
import cv2
import math
from PIL import Image
from os import listdir
import pytesseract
import tesseract
import time

import mechanize

startTime = time.time()

counter = 0;

browser = mechanize.Browser()

browser.set_handle_robots(False)

baseUrl = "https://www.viacar.ch/eindex/login.aspx?kanton=zh"
captchaUrl = "https://www.viacar.ch/eindex/JpegGenerate.aspx"

while(True):
   browser.open(baseUrl)
   captchaOrig = browser.open_novisit(captchaUrl).read()

   with open("temp.jpg", "wb") as file:
       file.write(captchaOrig)
   temp = cv2.imread("temp.jpg")
   cv2.imshow('temp',temp)

   cv2.waitKey(1)
   print time.time()-startTime
   print "Bitte Code eingeben"
   solution = raw_input()

   with open("raw\\" + str(solution)+ ".jpg", "wb") as file:
       file.write(captchaOrig)

cv2.waitKey()



#print img.read()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

total = 0.0
correct = 0.0

while (True) :
   cv2.waitKey()

cv2.destroyAllWindows()
