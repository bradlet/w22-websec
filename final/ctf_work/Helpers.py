import sys
import requests
from bs4 import BeautifulSoup


# Pull site info from cli args -- drop https:// if included
def parseArgsForSite(site_if_absent):
    s = site_if_absent
    if len(sys.argv) == 2:  # Use cli arg if present
        s = sys.argv[1]
    if 'https://' in s:
        s = s.rstrip('/').lstrip('https://')
    return s


# Wraps the process of grabbing the exploit link and stores the provided `payload`
# in the exploit server.
def uploadExploit(session, site, payload, action):
    url = f'https://{site}/'
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')
    form_data = {
        'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
        'responseBody': payload,
        'formAction': action
    }
    return session.post(exploit_url, data=form_data)


# Simple html search in response text
def searchResponse(resp, search_for):
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup.find(search_for)


# Just a helper to make sure that timeouts are clearly communicated, avoiding any
# mental overhead when already focused on solving some CTF.
def checkForSiteLiveness(site):
    resp = requests.get(f'https://{site}')
    if resp.status_code == 504:
        print("Site timed out, refresh then try again.")
        exit()
