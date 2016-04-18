#! /usr/bin/env python3
# ilovedanielpinkwater.py
# remember to donate some money to Daniel since you're enjoying all his audiobooks.

import requests
import os
import bs4
import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()
browser.get('http://www.pinkwater.com/podcast/audioarchive.php')
'''
#form_elem = browser.find_element_by_tag_name('form')
try:
    element = webDriverWait(browser, 15).until(EC.presence_of_all_elements_located(By.tag,'Option'))
finally:
    browser.quit()
'''
book_elem = browser.find_elements_by_tag_name('Option')

#book_elem[3].submit()
#mp3_link = browser.find_elements_by_partial_link_text('Chapter')

os.mkdir('/Users/han/Desktop/Daniel Pinkwater Audiobooks')

for book_page in book_elem:
    book_page.submit()
    mp3_links = browser.find_elements_by_partial_link_text('Chapter')

    if len(mp3_links) < 1:
        mp3_links = browser.find_elements_by_partial_link_text('Entire book')

    for chapter in mp3_links:
        chapter.click()
        mp3_response = requests.get(browser.current_url)
        mp3_response.raise_for_status()
        #add book title to file or go fancy and figure out how to add title/author/type as mp3 meta-info
        #eyeD3
        
        file_name = os.path.split(browser.current_url)[1]

        with open(file_name, 'wb') as f:
            for chunk in mp3_response.iter_content(100000):
                f.write(chunk)

        browser.back()

browser.close()
#example file path
#http://www.pinkwater.com/podcast/archive/bobowicz1-4.mp3

'''
make a directory to save all the book files
and go to it
make a file to save a book file

open the file path
save the file
check that it worked
close the file

'''

'''

try:
    dan_response.raise_for_status()
except Exception as e:
    print('There was a problem {}' .format(e))

audiobook_chapter = open('Pinkwater_Chapter.mp3', 'wb') 

for chunk in dan_response.iter_content(chunk_size = 100000):
    audiobook_chapter.write(chunk)

audiobook_chapter.close()
'''
'''
# form action has all the files for http://www.pinkwater.com/podcast/audioarchive.php

dan_response = requests.get('http://www.pinkwater.com/podcast/audioarchive.php', 'html.parser')

books = []

dan_soup = bs4.BeautifulSoup(dan_response.text)
for book in dan_soup.find_all('option'): 
    books.append((book.get('value')))

'''
