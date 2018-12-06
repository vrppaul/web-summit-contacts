import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

data = pd.read_csv('startup.csv')
data['emails'] = np.nan

os.system(f'python python-sitemap-master/main.py --domain {data.startupSite[0]} --output sitemap.xml')
while True:
    contact_url = ''
    list_of_emails = []
    infile = open("sitemap.xml","r")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    urls = soup.find_all('loc')
    for url in urls:
        if '/contact' in url.get_text():
            contact_url = url.get_text()
            break
    if len(contact_url):
        req = Request(contact_url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')
        list_of_emails = soup.find_all(string=re.compile(f"@{data.startupSite[0][len('http://www.'):-1]}"))
    infile.close()
    if len(list_of_emails):
        os.system('^C')
        data.emails[1] = list_of_emails
        break
