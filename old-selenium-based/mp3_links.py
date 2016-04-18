#! /usr/bin/env python3
# Download all the free Daniel Pinkwater audiobooks he's posted to a desktop folder.  
#remember to donate some money to Daniel since you're enjoying all his audiobooks.

import requests
import os
import webbrowser
from selenium import webdriver
import time 

browser = webdriver.Firefox()
browser.get('http://www.pinkwater.com/podcast/audioarchive.php')

#These browser element objects get erased and need to be re-created in the "for" loops. Why?

#Audiobooks
book_elem = browser.find_elements_by_tag_name('Option')
#
mp3_links = browser.find_elements_by_partial_link_text('Chapter')

if not os.path.exists('~/Desktop/Daniel Pinkwater Audiobooks'):
    os.mkdir('~/Desktop/Daniel Pinkwater Audiobooks')

#I tried to write this more elegantly as
#for book in book_elem:
#but that didn't work at all -- because it's not the right type of object?

#also, I don't understand why I need to recreate the objects from "browser.find"

for book in range(len(book_elem)):
    book_elem[book].submit()
    mp3_links = browser.find_elements_by_partial_link_text('Chapter')

    if len(mp3_links) < 1:
        mp3_links = browser.find_elements_by_partial_link_text('Entire book')
    
    print(book, "book")
    print("In the book there are {} sections" .format(len(mp3_links)))

    for chapter in range(len(mp3_links)):
        print("Chapter ", chapter," type ", type(mp3_links[chapter]))
        
        mp3_links[chapter].click()
        browser.back()
        mp3_links = browser.find_elements_by_partial_link_text('Chapter')
        

    book_elem = browser.find_elements_by_tag_name('Option')
