'''
    Converts html file from specific url to text
'''
import os
import sys
import subprocess
import math

# pip necessary modules 
piped_modules = subprocess.check_output(['python', '-m', 'pip', 'list']).decode()
if 'bs4' not in piped_modules: subprocess.call("python -m pip install bs4")
if 'unidecode' not in piped_modules: subprocess.call("python -m pip install unidecode")

import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
path_to_script_dir = os.path.dirname(os.path.abspath(__file__))


def numToWord(num):
    numDict = {
        # there will never be a chapter zero, but this is needed
        # for numbers whos ones place of is zero (10, 20, 30, ...)
        '0': '', 
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        '10': 'ten',
        '11': 'eleven',
        '12': 'twelve',
        '13': 'thirteen',
        '14': 'fourteen',
        '15': 'fifteen',
        '16': 'sixteen',
        '17': 'seventeen',
        '18': 'eighteen',
        '19': 'nineteen'
    }

    tensDigitDict = {
        '2': 'twenty',
        '3': 'thirty',
        '4': 'fourty',
        '5': 'fifty',
        '6': 'sixty',
        '7': 'seventy',
        '8': 'eighty',
        '9': 'ninety'
    }

    if num < 20:
        # since numbers 1-20 are weird have to hard code them
        toReturn = numDict[str(num)]
    
    elif num >= 20:
        # get the number that is contained in the tens and one digit
        tensDigit = math.trunc(num/10)
        onesDigit = num % 10 # mod by ten to get one's digit

        prefix =  tensDigitDict[str(tensDigit)]
        suffix = numDict[str(onesDigit)]

        if onesDigit != 0:
            toReturn = prefix + '-' + suffix
        else:
            toReturn = prefix

    return toReturn

url_base = "http://novel68.com/dune/"
url_list = []

# Parse through all urls and add them to list
for i in range(30): # there are thirty chapters
    # ----- need to convert chapter number to words for url------#
    chapter_num_in_words = numToWord(i+1)  # book starts from chapter 1, not chapter 0
    full_url = url_base + 'chapter-' + chapter_num_in_words
    url_list.append(full_url)


# add appendixes (there are 4 of them)
appendix1 = url_base + "appendix-i-the-ecology-of-dune"
appendix2 = url_base + "appendix-ii-the-religion-of-dune"
appendix3 = url_base + "appendix-iii-report-on-bene-gesserit"
appendix4 = url_base + "appendix-iv-the-almanak-en-ashraf"
url_list.append(appendix1)
url_list.append(appendix2)
url_list.append(appendix3)
url_list.append(appendix4)
# print(url_list)
#---------------------------DONE GETTING ALL LINKS-----------------------#


#-----------------PULL TEXT FROM EACH URL----------------------#
book = []
for url_num, url in enumerate(url_list):

    print("Loading txt from url " + url)
    
    # sometimes need to make a request before extracting from url
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    page_start_index = 0
    page_end_index = 0
    lines = text.splitlines()

    # print(text)

    # Parse through page and check for key words that mark the beg and end of the page
    # This will always mark the beginining of the page
    if url_num == 0:
        # first page is different
        beg_phrase = "        Next Book One"
    else:
        beg_phrase = "        Next "
    end_phrase = "Loading...     Prev"
    page_start_index = text.index(beg_phrase) + len(beg_phrase) 
    page_end_index = text.index(end_phrase)

    print("Start index: {0}\nEnd Index: {1}".format(page_start_index, page_end_index))

    # If not the first chapter/page, then dont show title again
    # Use line numbers found to get rid of useless parts of book
    writeable_text = text[page_start_index:page_end_index]
    book.append(writeable_text)
    # print(writeable_text)

name_of_txt_file = "Dune (Book 1)"
path_to_txt_file = os.path.join(path_to_script_dir, 'SavedBooks', name_of_txt_file)

# Save text converted html to a file
with open(path_to_txt_file, 'w+') as write_file:
   writeable_text = "\n".join(book)
   writeable_text = unidecode(writeable_text)
   write_file.write(writeable_text)

