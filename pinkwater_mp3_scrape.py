"""Pull Daniel Pinkwater audiobooks off his website."""

import requests
import os
import webbrowser
import re
import json
from bs4 import BeautifulSoup, SoupStrainer #requires lxml
from fake_useragent import UserAgent
import mutagen

#change to absolute path
DOWNLOAD_DIR = 'DanielPinkwaterAudiobooks'
#make constant for web page

def get_book_list():
    ''' Get list of all audiobooks from drop-down options
    '''
    booklist = 'booklist.json'

    if os.path.exists(booklist):
        with open(booklist, 'r') as f:
            return json.load(f)

    r = requests.get('http://www.pinkwater.com/podcast/audioarchive.php')
  
    strainer = SoupStrainer('option')
    indexsoup = BeautifulSoup(r.text, 'lxml', parse_only=strainer)
    
    book_options = []
    for book in indexsoup.find_all('option'):
        book_options.append(book.text)

    with open(booklist, 'w') as f:
        json.dump(book_options, f)

    return book_options

def get_book_page(book_option):
    ''' Should: 
    Make a directory for storing individual web pages for each book if it doesn't exist.
    Save audiobook-specific page with audiobook chapters/mp3 files
    
    ''' 
    #get html, parameter is url. try passing in URL to post/cache at same time - use for html and mp3s.
    book_html = ''
    #Should I return file path or text (not sure how to get that)
    #return file.read

    #check if page is already cached, save if not
    book_html_filename = get_filesafe_name(book_option, '.html')
    book_html_dir = 'bookpages'
    book_html_relativepath = os.path.join(book_html_dir, book_html_filename)

    filepath_check(book_html_dir)

    if not os.path.exists(book_html_relativepath):
        #Write the file to the directory
        #book_option = 'Adventures+of+a+Cat-Whiskered+Girl'
        headers = { 'User-Agent' : UserAgent().firefox }
        data = {'thebook' : book_option }
        
        #data = 'thebook=Adventures+of+a+Cat-Whiskered+Girl'
        response = requests.post('http://www.pinkwater.com/podcast/audioarchive.php', headers=headers, data=data)
        book_html = response.text
        with open(book_html_relativepath,'w') as file:
            file.write(response.text)
    else:
        with open(book_html_relativepath, 'r') as file:
            book_html = file.read() 
    #return text instead of path
    return book_html

def get_mp3_urls(book_html):
    ''' Get the urls for each chapter of the audiobook from webpage.
    Write each chapter to file.
    '''

    strainer = SoupStrainer('a')
    book_page_soup = BeautifulSoup(book_html, 'lxml', parse_only=strainer)

    #Extract URLs and return them
    mp3_urls = []

    for link in book_page_soup:
        #use hasattr(link, 'attrs')
        if 'attrs' in link.__dict__.keys() and 'href' in link.attrs and 'mp3' in link.attrs['href']:
            url = 'http://www.pinkwater.com/podcast/' + link.attrs['href']
            mp3_urls.append([url,link.text])

    return mp3_urls

def get_mp3s(mp3_urls, book):
    filesafe_book = get_filesafe_name(book)

    #Make directory for chapter files for each audiobook
    book_folder = get_filesafe_name(book)
    book_folder_path = os.path.join(DOWNLOAD_DIR, book_folder)
    filepath_check(book_folder_path)

    for url, chapter in mp3_urls: 
        filesafe_mp3name = get_filesafe_name(chapter)
        mp3_name = filesafe_book+'_'+filesafe_mp3name+'.mp3'
         
        #Exit function if file is already saved.
        mp3_path = os.path.join(book_folder_path, mp3_name)

        if os.path.exists(mp3_path):
            continue

        response = requests.get(url)

        with open(mp3_path,'wb') as file:
            file.write(response.content)

def make_book_directory(book):
    ''' Make a DanielPinkwaterAudiobook folder, and make individual book folder
    to hold the multiple chapter audiobook files for each book.
    '''

    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    book_folder = get_filesafe_name(book)
    book_folder_path = os.path.join(DOWNLOAD_DIR, book_folder)
    
    filepath_check(book_folder_path)

    return book_folder_path

def get_filesafe_name(name, suffix=''):
    reg = re.findall('\w*', name)
    filesafe_name = '_'.join(reg).rstrip('_') + suffix

    return filesafe_name

def filepath_check(path):
    if os.path.exists(path):
        return 
    
    os.mkdir(path)

def label_mp3(filepaths, book):
    ''' Give file ID3 labels.
    '''
    mp3_tags = {'artist':'Daniel Pinkwater', 'album':book, 'genre':'Books & Spoken'}
    
    for path in filepaths:
        print(path)
        sound_object = AudioSegment.from_file(path, format='mp3')
        sound_object.export(path, tags=mp3_tags, format='mp3')

def main():
    ''' Get audiobook files from Daniel Pinkwater's site.
    '''
    #Get list of book options from drop down menu on main page
    book_options = get_book_list()

    #Make folder to hold all individual book folders
    filepath_check(DOWNLOAD_DIR)

    for book in book_options:
        print(book)

        #Get cached or requested html file with audiobook mp3 chapters listed
        #get_html_for_book(book)
        mp3s_page = get_book_page(book)

        print('getting mp3s')
        
        #Parse out mp3 URLs from html
        mp3_urls = get_mp3_urls(mp3s_page)

        #Save mp3 if not already saved.
        get_mp3s(mp3_urls, book)
        
        print('labelling book')
        
        # #Reopen file and give ID3 labels.
        # label_mp3(mp3_paths, book)

if __name__ == '__main__':
    main()
        