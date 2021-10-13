

import requests #to access to the page content
import datetime
import nltk
import re
import time


from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

nltk.download('punkt')

#URL of product scan
URL = 'https://www.amazon.es/AMD-Ryzen-5-5600X-Box/dp/B08166SLDF/ref=sr_1_1?'

#User agent
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320'}

#now we can do requests
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser') #obtains page content with soup



domain = re.search("(www)\.([A-Za-z0-9\-\.]+)(\.es|\.com)", URL).group() #obtains domain form URL source with expReg

def scanStock():
    actualTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-7] #obtains the actual time without decimals

    title = soup.find(id="productTitle").get_text().strip()  # obtains the id content (title)
    titleFilter = word_tokenize(str(title))[:10] #Using the nltk library, filters the product title to obtain first 10 words
    showTitle = ' '.join(titleFilter) #concatenates the words obtaining the reduced title

    #print(title)  # Shows the title

    stock = soup.find(id='availability').get_text().strip()  # obtains the id content (availability) and delete spaces with strip()

    if (stock == "En stock."): #If there's stock then show the alert
        price = soup.find(id="priceblock_ourprice").get_text()  # obtains the product price by id
        print('<', actualTime, '>', '[', domain, ']' , '[', showTitle, '] --> (ALERT) Product IN STOCK', '(', price, ')')
    else:
        print('<', actualTime, '>', '[', domain, ']', '[', showTitle, '] --> (i) Product without stock')

#-- End scanStock

while(True): #Scan product each second
    scanStock()
    time.sleep(1)
