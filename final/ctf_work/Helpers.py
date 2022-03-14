import sys
from bs4 import BeautifulSoup


# Pull site info from cli args -- drop https:// if included
def parseArgsForSite():
    try:
        s = sys.argv[1]
        if 'https://' in s:
            s = s.rstrip('/').lstrip('https://')
        return s
    except IndexError:
        raise IndexError("Need to provide site URL when running script")


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

