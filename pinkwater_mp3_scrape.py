"""Pull Daniel Pinkwater audiobooks off his website."""

import requests
import os
import webbrowser
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent

def main:
    '''
    Get options for books
    send book selection in header
    Get URLs of each book chapter
    Cache in file
    make folder for book in directory if doesn't exist
    check if chapter mp3 file exists
    get if doesn't exist  
    '''

    if not os.path.exists('./DanielPinkwaterAudiobooks'):
        os.mkdir('DanielPinkwaterAudiobooks')
    os.path.join(DanielPinkwaterAudiobooks)
    if not os.path.exists('./DanielPinkwaterAudiobooks/audiobook_list'):
        os.path.join()
r = requests.get('http://www.pinkwater.com/podcast/audioarchive.php')

strainer = SoupStrainer('option')
indexsoup = BeautifulSoup(r.text, 'lxml', parse_only=strainer)
audiobook_list = [ book.text for book in indexsoup.find_all('option')]

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


if __name__ == '__main__':
    main()
        