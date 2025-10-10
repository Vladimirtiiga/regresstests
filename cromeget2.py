import requests
import json
import zipfile
import os
import shutil
from os import path
#import wget
def getupdate():

    url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
    response = requests.get(url)
    #print(json.load(response.content))
    with open('last-known-good-versions-with-downloads.json', 'wb') as file:
        file.write(response.content)

    with open('last-known-good-versions-with-downloads.json', "r") as fh:
        newdict = json.load(fh)

    newdictchanels=newdict['channels']
    newdictchanelsstable=newdictchanels['Stable']
    newdictchanelsstabledownloads=newdictchanelsstable['downloads']
    newdictchanelsstabledownloadscromedriver=newdictchanelsstabledownloads['chromedriver']
    #print(newdictchanelsstabledownloadscromedriver)
    for spisok in newdictchanelsstabledownloadscromedriver:
        if spisok['platform']=='win64':
            print(spisok['url'])
            url2=spisok['url']

    #wget.download('https://lenta.com/contentassets/413fc8748e5c4b95a2a8f2b99a274ce5/LN15_katalog_SM_SZFO_OMNI.pdf')
    response = requests.get(url2)
    with open('chromedriver-win64.zip', 'wb') as file:
        file.write(response.content)

    fzip = zipfile.ZipFile('chromedriver-win64.zip')
    fzip.extractall('')
    fzip.close()

    src = path.realpath("chromedriver-win64\\chromedriver.exe")
    dst = "chromedriver.exe"
    shutil.copy(src, dst)