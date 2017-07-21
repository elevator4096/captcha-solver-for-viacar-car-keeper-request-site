
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import ActionChains
import unittest, re
import pyautogui
import numpy as np
import cv2
import math
from PIL import Image
from os import listdir
import os
import pytesseract
import time
import mechanize
import Queue
#from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import re
import threading
import pandas as pd
import pickle

import fetch_mod

login_active = False

userhome = os.path.expanduser('~')
username = os.path.split(userhome)[-1]

webdriverPath = 'C:\Python27\webdrivers\chromedriver.exe'

if (username=="mani"):
   downloadPath  = "C:\Users\mani\Documents\Downloads\JpegGenerate.jpg"
elif (username=="user"):
   downloadPath  = "C:\Users\user\Downloads\JpegGenerate.jpg"

dictMsgStr = {"search"   : "Suchen Sie den Halter oder die Halterin durch die Eingabe der Kontrollschildnummer im nachstehenden Feld.",
              "wait"     : "Ihre Anfrage wird verarbeitet ....",
              "limit"    : "Sie haben die Anzahl zulässiger Abfragen für heute erreicht.",
              "result"   : "Suchergebnis f",
              "timeout"  : "Die Zeit ist abgelaufen, bitte neu anmelden.",
              "noresult" : "Das Suchergebnis ist negativ ausgefallen.",
              "login"    : "r die Anmeldung die oben angezeigte Nummer ein."
              }
#List of license numbers and owner : [(licenseNumber,owner),...]
ownerList = []
driver_threads = []
license_number_queue = Queue.Queue()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def init():
   #licenseNumbers = [412701,325048,658977,901934,453460,465005,224224,789004,591266,673524,395733,389937,282756,116784]
   licenseNumbers = []
   for i in range(1,2000):
      licenseNumbers.append(i)
   for licenseNumber in licenseNumbers:
      license_number_queue.put(licenseNumber)

def makelist(table):
  result = []
  allrows = table.findAll('tr')
  firstItem = True
  for row in allrows:
    result.append([])
    allcols = row.findAll('td')
    for col in allcols:
      #do not add the first item(its an empty list)
      if firstItem :
         firstItem = False
         continue
      thestrings = [unicode(s) for s in col.findAll(text=True)]
      thetext = ''.join(thestrings)
      regex = re.compile(r'[\n\r\t]')
      thetext = regex.sub('', thetext)
      result[-1].append(thetext)
  return result

def save_car_owner(driver,licenseNumber):
   time.sleep(1)        
   
   driver.find_element_by_id("TextBoxKontrollschild").clear()
   driver.find_element_by_id("TextBoxKontrollschild").send_keys(licenseNumber)
   driver.find_element_by_id("ButtonSuchen").click()
   time.sleep(1)
   source = driver.page_source
   
   if (source.find(dictMsgStr["noresult"])!= -1):
      print "No result for license number: " + str(licenseNumber)
      ownerList.append([[u'Art:', u''],[u'Name:', u''], [u'Strasse:', u''], [u'Ort:', u''], ['LicenseNumber:', licenseNumber]])
      driver.find_element_by_id("ButtonWeiter").click()
      time.sleep(0.5)
      return True
   
   if (source.find(dictMsgStr["result"])== -1):
      print "Error strange page for license number: " + str(licenseNumber)
      return False
      
   driver.find_element_by_id("ButtonWeiter").click()
   
   
   soup = BeautifulSoup(source)
   tables = soup.find("table", attrs={"bgcolor":"whitesmoke"})

   ownerData = makelist(tables)
   ownerData.append(["licenseNumber",licenseNumber])

   print ownerData
      
   ownerList.append(ownerData)
   return True
   
def solveCaptcha():

   watchdog = time.time()
   while not (os.path.isfile(downloadPath)):
      if (time.time()-watchdog)>8:
         return None
         
      time.sleep(0.05)
   time.sleep(0.1)

   frame = cv2.imread(downloadPath)

   ret,thresh = cv2.threshold(frame,80,255,cv2.THRESH_BINARY)
   thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
   denoise = cv2.fastNlMeansDenoising(thresh,searchWindowSize=18,h=65);

   return pytesseract.image_to_string(Image.fromarray(denoise),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 8" )

def new_driver_thread(PROXY):
    #PROXY = "213.233.57.135:80" # IP:PORT or HOST:PORT
    #PROXY = "45.58.34.170:3128" # IP:PORT or HOST:PORT
    #driver = webdriver.Chrome()
    global login_active

    #start of critical section(focus needed)
    login_active = True
      
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_argument("--window-size=400,600")
    driver = webdriver.Chrome(webdriverPath,chrome_options=chrome_options)
    driver.implicitly_wait(60)
    
    base_url = "https://www.viacar.ch"
    verificationErrors = []
    accept_next_alert = True

    success = False
    driver.get(base_url + "/eindex/Login.aspx?Kanton=ZH")
    source = driver.page_source
    #if we don't get to the login page something is fishy with the proxy
    if (source.find(dictMsgStr["login"])== -1):
       login_active = False
       driver.quit()
       time.sleep(1)
       return

    while not success:

        try:
            os.remove(downloadPath)
        except:
            pass
    
        SecBild = driver.find_element_by_id("SecBild")

        
        ActionChains(driver) \
            .move_to_element(SecBild) \
            .context_click(SecBild) \
            .perform()

        
        pyautogui.press('down')
        time.sleep(0.2)
        pyautogui.press('down')
        time.sleep(0.2)
        pyautogui.press('enter')
        #time.sleep(1.5)
        #pyautogui.typewrite(downloadPath)
        #time.sleep(0.8)
        time.sleep(1)
        pyautogui.press('enter')
        
        source = driver.page_source

        searchStr = 'document.getElementById("'
        pos1 = source.find(searchStr)+len(searchStr)
        pos2 = source.find('"',pos1+1)
        input_id = source[pos1:pos2]   
         
        captchaSolution = solveCaptcha()
        #print captchaSolution

        if (captchaSolution==None):
           login_active = False
           driver.quit()
           time.sleep(1)
           return
        
        driver.find_element_by_id(input_id ).clear()
        driver.find_element_by_id(input_id ).send_keys(captchaSolution)
        time.sleep(0.1)
        driver.find_element_by_id("BtLogin").click()

        source = driver.page_source
        
        if (source.find(dictMsgStr["search"])== -1):
            success = False
            #if we are not back on the login page something is fishy with the proxy
            if (source.find(dictMsgStr["login"])== -1):
               login_active = False
               driver.quit()
               time.sleep(1)
               return
        else:
            #print "Success!!!"
            success = True   

    #End of critical section(no focus needed anymore)
    login_active = False
    source = driver.page_source
    while(source.find(dictMsgStr["search"])!= -1):       

       try:
          licenseNumber = license_number_queue.get_nowait()
       except Queue.Empty:
           driver.quit()
           time.sleep(1)
           return
         
       if (licenseNumber==None):
          driver.quit()
          time.sleep(1)
          return
         
       if not (save_car_owner(driver,licenseNumber)):
          #if we get a stange page instead of a result or noresult we store the license number back in the queue
          license_number_queue.put(licenseNumber)
       source = driver.page_source
       


    #time.sleep(5) # Pause to allow you to inspect the browser. 

    driver.quit()

def main():
   
   global login_active
   proxythread = threading.Thread(target=fetch_mod.main)
   proxythread.setDaemon(True)
   proxythread.start()
   init()
   time.sleep(8)
   initialActiveCount = threading.active_count()
   while not license_number_queue.empty():
      #get the next proxy
      while True:
       try:
           proxyItem = fetch_mod.get_queue().get()
           if proxyItem["type"]=="http":
               break
       except:
           print "no proxys available!!!"
           time.sleep(5)
 
      PROXY = str(proxyItem["IP"])+":"+str(proxyItem["PORT"])

      #wait with creating new thread until no login and less than x threads
      while (login_active or ((threading.active_count()-initialActiveCount) >= 6 )):
         time.sleep(0.1)
      driver_thread = threading.Thread(name="driver_thread",target=new_driver_thread, args=(PROXY,))
      driver_thread.start()
      driver_threads.append(driver_thread)
      #Yes we really have to wait over 30 seconds to catch all the results of the other threads
      time.sleep(50)


   for owner in ownerList:
      print owner

   with open('car_owners.pickle','wb') as f:
      pickle.dump(ownerList,f)


if __name__ == '__main__':
   start = time.time()
   print "start"
   main()
   print "time: " + str(time.time()-start)
