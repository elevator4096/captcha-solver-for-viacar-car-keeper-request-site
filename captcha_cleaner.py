import numpy as np
import cv2
import math
from PIL import Image
from os import listdir
import pytesseract
#import tesseract
import time

import mechanize

startTime = time.time()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

total    = 0.0
corrects = np.zeros(8,dtype=np.float)

lenSum = 0.0


for filename in listdir("original"):

   if filename[-3:] != "jpg" : continue; 
   #print (filename)
   total += 1
   
   frame = cv2.imread("original\\"+filename)
   #frame = cv2.imread("C:\Users\mani\Dropbox\elevator4000\Captcha.jpg")
   ret,thresh = cv2.threshold(frame,80,255,cv2.THRESH_BINARY)
   thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
   
   #edge = cv2.Canny(frame, 120, 255)
   #edgeBlur = cv2.GaussianBlur(edge,(11,11),0)

   kernel = np.ones((2,2),np.uint8)
   #dilate = cv2.dilate(thresh,kernel,iterations = 1)
   #ret,thresh = cv2.threshold(edgeDilated,50,255,0)

   denoise0 = cv2.fastNlMeansDenoising(thresh,searchWindowSize=18,h=65);
   #denoise0 = cv2.GaussianBlur(denoise0,(3,3),0)
   ret,denoise0 = cv2.threshold(denoise0,200,255,cv2.THRESH_BINARY_INV)
   
   
   #_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   _, contours, hierarchy = cv2.findContours(denoise0,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   mask = np.zeros(thresh.shape, np.uint8)
   numOfContours = 0
   if len(contours) != 0:
      biggestContour = contours[0]
      biggestContourArea = 0
      i = -1
      for c in contours:
         i = i+1
         #if i == 0:continue
         Area = cv2.contourArea(c)
         if (Area < 40): continue
         if (Area > 500): continue
         if hierarchy[0,i,3] != -1 : continue
         x,y,w,h = cv2.boundingRect(c)
         #if h<10: continue
         
         cv2.drawContours(mask, [c], 0, (255), -10)
         cv2.drawContours(frame, [c], 0, (0,255,0), 1)
         cv2.imshow('frame',frame)
         cv2.waitKey()

         numOfContours = numOfContours+1
         
         if Area > biggestContourArea:
            biggestContour = c
            biggestContourArea = Area

         
      #cv2.drawContours(frame, [biggestContour], 0, (0,255,0), 3)
      x,y,w,h = cv2.boundingRect(biggestContour)
      #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
   print numOfContours
      

   #cv2.circle(frame, maxLoc, 4, (0, 0, 255), 2)
   
   #final = thresh2;

   threshTemp = cv2.bitwise_not(thresh)
   masked = cv2.bitwise_and(threshTemp,mask, mask = mask)
   masked = cv2.bitwise_not(masked)
  
   
   denoise1 = cv2.fastNlMeansDenoising(thresh,searchWindowSize=18,h=65);
   
   denoise2 = denoise0
   """
   denoise3 = cv2.GaussianBlur(thresh,(3,3),0);
   denoise4 = cv2.GaussianBlur(masked,(5,5),0);
   denoise5 = cv2.GaussianBlur(thresh,(7,7),0);
   denoise6 = cv2.GaussianBlur(masked,(9,9),0);
   denoise7 = cv2.GaussianBlur(thresh,(11,11),0);
   denoise8 = cv2.GaussianBlur(masked,(1,1),0);
   """

   
   cv2.imshow('frame',frame)
   cv2.imshow('masked',masked)
   cv2.imshow('thresh',thresh)
   cv2.imshow('mask',mask)
   cv2.imshow('d1',denoise1)
   cv2.imshow('d0',denoise0)
   

   #cv2.imshow('dilate',dilate)
   #cv2.imshow('d1',denoise1)
   #cv2.imshow('d2',denoise2)
   #cv2.imshow('d3',denoise3)

   cv2.waitKey()
   
   #cv2.imshow('thres2h',thresh2)
   
   #cv2.imwrite("clean\\"+filename, denoise1)
   #cv2.imwrite("denoise4\\"+filename, denoise4)
   #cv2.imshow('edge',edge)
   #cv2.imshow('thresh',thresh)

   #cv2.imshow('thresh',threshold)

   """
   help(tesseract)
   api = tesseract.TessBaseAPI()
   api.Init(".","eng",tesseract.OEM_DEFAULT)
   api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz")
   api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
   tesseract.SetCvImage(denoise,api)
   print (api.GetUTF8Text() )
   """
   
   resultStrings = []
    
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise1),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   """
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise2),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise3),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise4),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise5),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise6),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise7),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   resultStrings.append( pytesseract.image_to_string(Image.fromarray(denoise8),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" ) )
   """

   print resultStrings
   print filename[:-4]

   i = 0
   for s in resultStrings:
      if (s == filename[:-4]):
         corrects[i] += 1
         lenSum += len(filename)-4
         
      i += 1
   
   k = cv2.waitKey(30) & 0xff 
   if k == 27:
      break

print corrects
print total
print (corrects/total)
print time.time() - startTime
#print lenSum/corrects[0]
#while (True) : pass

cv2.destroyAllWindows()
