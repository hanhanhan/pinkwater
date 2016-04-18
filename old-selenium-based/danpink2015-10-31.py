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

if not os.path.exists('/Users/han/Desktop/Daniel Pinkwater Audiobooks'):
    os.mkdir('/Users/han/Desktop/Daniel Pinkwater Audiobooks')

#I tried to write this more elegantly as
#for book in book_elem:
#but that didn't work at all -- because it's not the right type of object?
for book in range(len(book_elem)):
#for book in range(min(3,len(book_elem))):

    book_elem[book].click()
    book_elem[book].submit()
    #this disappears unless I recreate it. why?
    mp3_links = browser.find_elements_by_partial_link_text('Chapter')
    print(book, "th book")
    print("In the book there are {} sections" .format(len(mp3_links)))

    if len(mp3_links) < 1:
        mp3_links = browser.find_elements_by_partial_link_text('ntire book')
    if len(mp3_links) < 1:
        mp3_links = browser.find_elements_by_partial_link_text('Part')        

    #for chapter in range(len(mp3_links)):
    for chapter in range(min(1,len(mp3_links))):
        print("in the chapter loop, round ", chapter)
        mp3_links = browser.find_elements_by_partial_link_text('Chapter')
        
        if len(mp3_links) < 1:
            mp3_links = browser.find_elements_by_partial_link_text('ntire book')
        if len(mp3_links) < 1:
            mp3_links = browser.find_elements_by_partial_link_text('Part')

        print("Chapter ", chapter)
        mp3_links[chapter].click()
        #what is this built in function/method with no braces at the end? 
        mp3_url = browser.current_url
        mp3_response = requests.get(mp3_url)
        #add book title to file or go fancy and figure out how to add title/author/type as mp3 meta-info
        #eyeD3
        file_name = os.path.split(mp3_url)[1]
        print("File ",file_name)

        mp3_file = os.path.split(mp3_url)[1]
        directory = "/Users/han/Desktop/Daniel Pinkwater Audiobooks"
        file_path = os.path.join(directory,mp3_file)

        with open(file_path, 'wb') as f:
            for chunk in mp3_response.iter_content(100000):
                f.write(chunk)

        browser.back()
        
        print(len(mp3_links), "# of chapter")
        book_elem = browser.find_elements_by_tag_name('Option')
        