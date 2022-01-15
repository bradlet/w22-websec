import requests
import multiprocessing
from bs4 import BeautifulSoup

# Local module imports
from timeDecorator import time_decorator


def getUrlTitle(url):
    """
    This function returns the <title> of an HTML document given its URL
    :param url: URL to retrieve
    :type url: str
    :return: Title of URL
    :rtype: str
  """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = str(soup.find('title'))
    return title


@time_decorator
def getSequential(urls):
    """
    Given a list of URLs, retrieve the title for each one using a single synchronous process
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :return: list of titles for each URL
    :rtype: list of str
    """
    titles = []
    for u in urls:
        titles.append(getUrlTitle(u))
    return titles


# Runs getSequential in parallel w/ N (== num_processes) processes.
@time_decorator
def getMulti(urls, num_processes):
    p = multiprocessing.Pool(num_processes)
    titles = p.map(getUrlTitle, urls)
    p.close()
    return titles


# Added this so that I could run in PyCharm w/ the play button.
if __name__ == '__main__':
    urls = [
        'https://pdx.edu',
        'https://oregonctf.org',
        'https://google.com',
        'https://facebook.com',
        'https://repl.it',
        'https://youtube.com',
        'https://wikipedia.org',
        'https://runescape.com',
        'https://oldschool.runescape.com/',
        'https://bumped.com'
    ]

    run_multi = True

    if run_multi:
        parallelization = [2, 5, 10]
        outputs = [f'[N={c}] getMulti time: {getMulti(urls, c):0.2f}' for c in parallelization]
        print(outputs)
    else:
        print(f'{getSequential(urls):0.2f}')
