from bs4 import BeautifulSoup
import requests
import os
import sys
import re
from collections import Counter

#scraper

def QC_crawler(book_dict):

    page_count = Counter()
    base = 'https://megatokyo.com/'
    url = 'https://megatokyo.com/strip/1'
    last_com = False
    book = 'I Stopped Reading this Comic Ten Years ago, why am I doing this now? Surely there are better uses for my time.'
    last_url = last_page_finder('https://megatokyo.com/index.php', base)

    while last_com == False:

        QC_com = requests.get(url)

        sheet_num = url[28:].zfill(4)

        if sheet_num in book_dict:
            book = book_dict[sheet_num]
            os.makedirs(book, exist_ok = True)
            

        comic_soup = BeautifulSoup(QC_com.content, 'html5lib')

        try:

            imgs = comic_soup.find_all('img', {'src':re.compile('strips/*')})

            com_down = f'{base}{imgs[0].get("src")}'

            image = requests.get(com_down)

            page_count[book] += 1

            sys.stdout.write(f'Downloading {book} page {page_count[book]} \n')
            sys.stdout.flush()

            com_name = f'{book} {str(page_count[book]).zfill(3)}{com_down[-4:]}'

            try: 
                image_file = open(os.path.join(book, os.path.basename(com_name)), 'wb')
            
                for chunk in image.iter_content(100_000):
                    image_file.write(chunk)

                image_file.close()
            
            except:
                sys.stdout.write(f'ERROR with {book} {page_count[book]}\n')
                sys.stdout.flush()
        except:
            sys.stdout.write(f'No comic at {url}')
            sys.stdout.flush()

       
        if url == last_url:
            sys.stdout.write('All done!\n')
            sys.stdout.flush()
            last_com =  True


        else:
            next_class = comic_soup.find(class_ = 'next')
            next_link = next_class.contents[0].get('href')
            url = f'{base}{next_link[2:]}'


def last_page_finder(index_url, base):
    index_page = requests.get(index_url)
    last_read = BeautifulSoup(index_page.content, 'html5lib')
    prev_class = last_read.find(class_ = 'prev')
    prev_list = prev_class.contents
    prev_link = prev_list[0].get('href')
    prev_url = f'{base}{prev_link}'
    prev_page = requests.get(prev_url)
    prev_read = BeautifulSoup(prev_page.content, 'html5lib')
    next_class = prev_read.find(class_ = 'next')
    next_link = next_class.contents[0].get('href')
    last_page = f'{base}{next_link[2:]}'
    return last_page

books = {'1373' : 'Beach Omake Preview',
        '0001' : 'Chapter 0',
        '0134' : 'Chapter 1',
        '0196' : 'Chapter 2',
        '0307' : 'Chapter 3',
        '0402' : 'Chapter 4',
        '0526' : 'Chapter 5',
        '0639' : 'Chapter 6',
        '0743' : 'Chapter 7',
        '0875' : 'Chapter 8',
        '0983' : 'Chapter 9',
        '1141' : 'Chapter 10',
        '1270' : 'Chapter 11',
        '1383' : 'Chapter 11',
        '1434' : 'Chapter 12',
        '0398' : 'Grand Theft Colo',
        '0516' : 'Grand Theft Colo',
        '0731' : 'Circuity',
        '0973' : 'unMod',
        '1126' : 'Full Megatokyo Panic',
                }

def main():
    QC_crawler(books)

if __name__ == '__main__':
    main()


