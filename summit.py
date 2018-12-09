# multiproc_test.py

import random
import time
import threading
import subprocess
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import signal
import os
import pandas as pd

global_flag = False
def sitemap_creating(url):
    print('starting sitemap creating')
    print(url)
    time.sleep(0.2)
    p = subprocess.Popen([
    'python', 'python-sitemap-master/main.py', '--domain', 
    f'{url}', '--output', 'sitemap.xml', '--exclude', '/products', '--exclude', '/brands'
    ])
    while True:
        if global_flag:
            pid = p.pid
            os.kill(pid, signal.SIGINT)
            print('process terminated')
            break

def debugging(i):
    print('starting xml scraping')
    time.sleep(0.2)
    existing_urls = []
    contact_url = ''
    list_of_emails = []

    if 'https' in data.startupSite[i]:
        prefix = 'https://www.'
    else:
        prefix = 'http://www.'

    global global_flag
    while True:
        infile = open("sitemap.xml","r")
        contents = infile.read()
        soup = BeautifulSoup(contents,'xml')
        urls = [p.text for p in soup.find_all('loc')]
        new_urls = set(urls) - set(existing_urls)
        existing_urls = urls
        # print(new_urls)
        for url in new_urls:
            if '/contact' in url:
                contact_url = url
        if len(contact_url):
            req = Request(contact_url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'html.parser')
            list_of_emails = soup.find_all(string=re.compile(f"@{data.startupSite[i][len(prefix):-1]}"))
            infile.close()
            data.emails.iat[i] = list_of_emails
            global_flag = True
            break


if __name__ == '__main__':
    data = pd.read_csv('startup.csv')
    data['emails'] = ''
    for i in range(4, 6):
        p1 = threading.Thread(target=sitemap_creating, args=(data.startupSite[i], ))
        p2 = threading.Thread(target=debugging, args=(i, ))

        p1.start()
        p2.start()

        p1.join()
        p2.join()

    # writer = pd.ExcelWriter('startups.xlsx')
    # data.to_excel(writer,'Sheet1')
    # writer.save()