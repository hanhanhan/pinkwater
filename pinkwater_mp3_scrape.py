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

    audiobook_index = [ book['value'] for book in indexsoup.find_all('option')]

    with open(booklist, 'w') as f:
        json.dump(audiobook_index, f)

    return audiobook_index

def get_book_page(book_option):
    ''' Does not return book specific page with mp3 file index
    '''
    #check if page is already cached, get if not
    book_html = get_filesafe_name(book_option)
    book_html_dir_name = 'bookpages'
    book_html_relativepath = os.path.join(book_html_dir_name, book_html)

    if not os.path.exists(book_html_dir_name):
        os.mkdir(book_html_dir_name)

    if not os.path.exists(book_html_relativepath):
        #Write the file to the directory
        #book_option = 'Adventures+of+a+Cat-Whiskered+Girl'
        headers = { 'User-Agent' : UserAgent().firefox }
        data = {'thebook' : book_option }
        #data = 'thebook=Adventures+of+a+Cat-Whiskered+Girl'
        response = requests.post('http://www.pinkwater.com/podcast/audioarchive.php', headers=headers, data=data)
        with open(book_html_relativepath,'w') as file:
            file.write(response.text)

def parse_page():

    #need to test the 'href'=True part
    strainer = SoupStrainer('a', 'href=True')
    book_page_soup = BeautifulSoup(r.text, 'lxml', parse_only=strainer)

    return book_page_soup

def get_filesafe_name(link):
    reg = re.findall('\w*', link)
    filesafe_name_url = ''.join(reg) + '.html'

    return filesafe_name_url

def get_mp3s(book_page_soup):

    audiobook_chapters = {}
    d
    for link in indexsoup.a:
        #either ue this or the strainer with 'href'=True
        #if 'href' in getattr(link, 'attrs', {}):
        if '.mp3' in link['href']:
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

    return(audiobook_subdirectory)

def main():
    '''
    Get options for books
    send book selection in header
    Get URLs of each book chapter
    Cache in file
    make folder for book in directory if doesn't exist
    check if chapter mp3 file exists
    get if doesn't exist  
    '''

    book_index = get_book_index()

    for book in book_index:
        pass
        #Get urls of mp3 files from page.
        #cache mp3 urls in subdirectory
        #get mp3 files for each book and stash in book directory



    '''
        book_elem = browser.find_elements_by_tag_name('option')



    #I tried to write this more elegantly as
    #for book in book_elem:
    #but that didn't work at all -- because it's not the right type of object?
    print("Type of book_elem is ",type(book_elem))
    print("Type of range(len(book_elem)) is ", type(range(len(book_elem))))

    for book in range(len(book_elem)):
    #for book in range(min(3,len(book_elem))):
        book_elem[book].click()
        book_elem[book].submit()

        r = requests.get(browser.current_url)
        booksoup = BeautifulSoup(r.text, 'html.parser')


        #Get links for each chapter
        #It would be better to search by .mp3 per page
        #this disappears unless I recreate it. why?
        mp3_links = browser.find_elements_by_partial_link_text('Chapter')
        if len(mp3_links) < 1:
            mp3_links = browser.find_elements_by_partial_link_text('ntire book')
        if len(mp3_links) < 1:
            mp3_links = browser.find_elements_by_partial_link_text('Part')

        print(book_elem[book], " the book")
        print("In the book there are {} sections" .format(len(mp3_links)))        

        for chapter in range(len(mp3_links)):
        #for chapter in range(min(1,len(mp3_links))):
            print("in the chapter loop, round ", chapter)

            mp3_links = browser.find_elements_by_partial_link_text('Chapter')
            
            if len(mp3_links) < 1:
                mp3_links = browser.find_elements_by_partial_link_text('ntire book')
            if len(mp3_links) < 1:
                mp3_links = browser.find_elements_by_partial_link_text('Part')

            print("Chapter ", chapter)
            mp3_links[chapter].click()

            mp3_url = browser.current_url
            mp3_response = requests.get(mp3_url)
            #add book title to file or go fancy and figure out how to add title/author/type as mp3 meta-info
            #eyeD3
            file_name = os.path.split(mp3_url)[1]
            print("File ",file_name)

            mp3_file = os.path.split(mp3_url)[1]
            directory = "./DanielPinkwaterAudiobooks"
            file_path = os.path.join(directory,mp3_file)

            with open(file_path, 'wb') as f:
                for chunk in mp3_response.iter_content(100000):
                    f.write(chunk)

            browser.back()
            
            print(len(mp3_links), "# of chapter")
            book_elem = browser.find_elements_by_tag_name('Option')
    '''

if __name__ == '__main__':
    main()
        