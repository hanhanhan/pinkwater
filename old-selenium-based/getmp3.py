#! /usr/bin/env python3
# ilovedanielpinkwater.py
# remember to donate some money to Daniel since you're enjoying all his audiobooks.

import requests
import os
import bs4
import webbrowser
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://www.pinkwater.com/podcast/archive/bobowicz5-6.mp3')

mp3_url = browser.current_url
mp3_response = requests.get(mp3_url)
#mp3_file = urllib2.urlopen(mp3_url).read()
#add book title to file or go fancy and figure out how to add title/author/type as mp3 meta-info
#eyeD3

mp3_file = os.path.split(mp3_url)[1]
directory = "/Users/han/Desktop/Daniel Pinkwater Audiobooks"
file_path = os.path.join(directory,mp3_file)

with open(file_path, 'wb') as f:
    for chunk in mp3_response.iter_content(100000):
        f.write(chunk)

browser.close()
#example file path
#http://www.pinkwater.com/podcast/archive/bobowicz1-4.mp3
