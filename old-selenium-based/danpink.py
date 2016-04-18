#! /usr/bin/env python3
# ilovedanielpinkwater.py
# remember to donate some money to Daniel since you're enjoying all his audiobooks.

import requests
import os
import webbrowser
from selenium import webdriver
import time 

browser = webdriver.Firefox()
browser.get('http://www.pinkwater.com/podcast/audioarchive.php')

book_elem = browser.find_elements_by_tag_name('Option')

mp3_links = browser.find_elements_by_partial_link_text('Chapter')

if not os.path.exists('/Users/han/Desktop/Daniel Pinkwater Audiobooks'):
    os.mkdir('/Users/han/Desktop/Daniel Pinkwater Audiobooks')

#I tried to write this more elegantly as
#for book in book_elem:
#but that didn't work at all -- because it's not the right type of object?
for book in range(len(book_elem)):
    book_elem[book].submit()
    mp3_links = browser.find_elements_by_partial_link_text('Chapter')

    if len(mp3_links) < 1:
        mp3_links = browser.find_elements_by_partial_link_text('Entire book')
    
    print(book, "book")
    print("In the book there are {} sections" .format(len(mp3_links)))
    browser.back()
    book_elem = browser.find_elements_by_tag_name('Option')

'''
    for chapter in range(len(mp3_links)):
        print("Chapter ", chapter)
        mp3_links[chapter].click()
        #what is this built in function/method with no braces at the end? 
        mp3_url = browser.current_url
        mp3_response = requests.get(mp3_url)
        #add book title to file or go fancy and figure out how to add title/author/type as mp3 meta-info
        #eyeD3
        file_name = os.path.split(mp3_url)[1]

        with open(file_name, 'wb') as f:
            for chunk in mp3_response.iter_content(100000):
                f.write(chunk)

        browser.back()
'''




