# captcha-solver-for-viacar-car-keeper-request-site 
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-Public_domain-red.svg)](https://wiki.creativecommons.org/wiki/Public_domain)

#### Description

This small Proof of Concept shows how easily the captchas on the viacar website for car owner requests (https://www.viacar.ch/eindex/login.aspx?kanton=zh) 
can be solved by applying some denoising and using Tesseract (version 3.05.01) to recognize the Letters.

Just for fun I added a proxy fetcher (https://github.com/stamparm/fetch-some-proxies) to circumvent the 5 requests per IP per Day limit,
to get around 600 requests per day.

--------

#### Install dependencies:

	pip install pytesseract
	pip install BeautifulSoup
	pip install regex
	pip install pyautogui
	pip install pillow
	pip install selenium

install opencv2 from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)

install Tesseract (I REALLY recommend version 3.05.01) from [here](http://digi.bib.uni-mannheim.de/tesseract ) (you need tesseract-ocr-setup-3.05.01.exe)
to "C:/Program Files (x86)/Tesseract-OCR/tesseract"
	
extract chromedriver.exe (ChromeDriver version 2.30) from [here](https://chromedriver.storage.googleapis.com/index.html?path=2.30/)
to C:\Python27\webdrivers\chromedriver.exe
or place it somewhere else and change the webdriverPath accordingly.

----

#### Usage:
just run captcha_solver.py with python2.7 and let the magic happen ;-)
