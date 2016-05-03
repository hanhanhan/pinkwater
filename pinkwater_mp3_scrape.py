"""Pull Daniel Pinkwater audiobooks off his website."""

import requests
import os
import webbrowser
import re
import json
from bs4 import BeautifulSoup, SoupStrainer #requires lxml
from fake_useragent import UserAgent
import mutagen
from mutagen.easyid3 import EasyID3

# file path
DOWNLOAD_DIR = 'DanielPinkwaterAudiobooks'
# constant for web page
DANIEL_PINKWATER_SITE = 'http://www.pinkwater.com/podcast/audioarchive.php'

def get_book_list():
    ''' Get list of all audiobooks from drop-down options
    '''
    booklist = 'booklist.json'

    if os.path.exists(booklist):
        with open(booklist, 'r') as f:
            return json.load(f)

    r = requests.get(DANIEL_PINKWATER_SITE)
  
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
    book_folder_path = make_book_directory(book)
    
    for url, chapter in mp3_urls: 
        filesafe_mp3name = get_filesafe_name(chapter)
        mp3_name = filesafe_book+'_'+filesafe_mp3name+'.mp3'
         
        #Exit function if file is already saved.
        mp3_path = os.path.join(book_folder_path, mp3_name)

        if os.path.exists(mp3_path) and os.stat(mp3_path).st_size > 0:
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

def label_mp3(book):
    ''' Give file ID3 labels.
    '''
    mp3_tags = {'artist':'Daniel Pinkwater', 
    'album':book, 'genre':'Books & Spoken'}

    book_folder_path = make_book_directory(book)
    
    for path in os.listdir(book_folder_path):
        chapter_path = os.path.join(book_folder_path, path)

        try:
            mp3_tags = EasyID3(chapter_path)
        except mutagen.id3.ID3NoHeaderError:
            mp3_tags = mutagen.File(chapter_path, easy=True)
            mp3_tags.add_tags()

        mp3_tags['artist'] = 'Daniel Pinkwater'
        mp3_tags['genre'] = 'Books & Spoken'
        mp3_tags['album'] = book

        mp3_tags.save()

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
        
        #Parse out mp3 URLs from html
        mp3_urls = get_mp3_urls(mp3s_page)

        #Save mp3 if not already saved.
        get_mp3s(mp3_urls, book)
        
        #Reopen file and give ID3 labels.
        label_mp3(book)

if __name__ == '__main__':
    main()
        