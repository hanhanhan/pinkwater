"""Pull Daniel Pinkwater audiobooks off his website."""

import requests
import os
import webbrowser
import re
import json
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent


def get_book_audiofiles_index():
    pass

def get_book_list():
    ''' Get list of all audiobook options
    '''
    booklist = 'booklist.json'

    if os.path.exists(booklist):
        with open(booklist, 'r') as f:
            return json.load(f)

    r = requests.get('http://www.pinkwater.com/podcast/audioarchive.php')
  
    strainer = SoupStrainer('option')
    indexsoup = BeautifulSoup(r.text, 'lxml', parse_only=strainer)

    book_options = [ book['value'] for book in indexsoup.find_all('option')]

    with open(booklist, 'w') as f:
        json.dump(book_options, f)

    return book_options

def get_book_page(book_option):
    ''' Does not return book specific page with mp3 file index
    '''
    #Should I return file path or text (not sure how to get that)

    #check if page is already cached, get if not
    book_html = get_filesafe_name(book_option)
    book_html_dir = 'bookpages'
    book_html_relativepath = os.path.join(book_html_dir, book_html)

    filepath_check(book_html_dir)

    if not os.path.exists(book_html_relativepath):
        #Write the file to the directory
        #book_option = 'Adventures+of+a+Cat-Whiskered+Girl'
        headers = { 'User-Agent' : UserAgent().firefox }
        data = {'thebook' : book_option }
        #data = 'thebook=Adventures+of+a+Cat-Whiskered+Girl'
        response = requests.post('http://www.pinkwater.com/podcast/audioarchive.php', headers=headers, data=data)
        with open(book_html_relativepath,'w') as file:
            file.write(response.text)

    #return response.text / how do I load this?
    return book_html_relativepath

def parse_page(book_html_relativepath):

    #need to test the 'href'=True part
    strainer = SoupStrainer('a', 'href=True')

    with open(book_html_relativepath, 'r') as file:
        book_page_soup = BeautifulSoup(file, 'lxml', parse_only=strainer)

    audiobook_chapters = {}
    
    for link in book_page_soup:
        #either ue this or the strainer with 'href'=True
        #if 'href' in getattr(link, 'attrs', {}):
        if '.mp3' in link['href']:
            get_filesafe_name(link.string)

            #Map URL to chapter title 
            #to test
            audiobook_chapters[ link['href'] ] = link.text

            #get file and save to directory
            #if it doesn't already exist

    return audiobook_chapters

def make_book_directory(book):
    ''' Make a DaneilePinkwaterAudiobook file, and make individual subdirectories
    to hold the multiple chapter audiobook files for each book.
    '''

    if not os.path.exists('DanielPinkwaterAudiobooks'):
        os.mkdir('DanielPinkwaterAudiobooks')
    
    cwd = os.getcwd()
    audiobook_subdirectory = os.path.join(cwd, 'DanielPinkwaterAudiobooks', book)
    
    if not os.path.exists(audiobook_subdirectory):
        os.mkdir(audiobook_subdirectory)

    return audiobook_subdirectory

def get_filesafe_name(link):
    reg = re.findall('\w*', link)
    filesafe_name_url = ''.join(reg) + '.html'

    return filesafe_name_url

def filepath_check(path):
    if os.path.exists(path):
        return True
    
    os.mkdir(path)
    return False

def main():
    ''' Get audiobook files from Daniel Pinkwater's site and save in 
    '''
    #Get list of book options from drop down menu on main page
    book_options = get_book_list()

    #Get page for book listing all mp3 audiobook chapters
    #Doesn't work yet
    for option in book_options:
        
        #Make directory for chapter files for each audiobook
        audiobook_dir = make_book_directory(option)
        
        #Get cached or requested html file with audiobook files
        mp3s_page = get_book_page(option)
        
        #Parse out mp3 URLs from html
        links_or_soup = parse_page(mp3s_page)
        
        #Loop through each mp3 url to make sure it's saved in directory
        get_mp3s(links_or_soup)

if __name__ == '__main__':
    main()
        