import asyncio
import requests
import multiprocessing
import matplotlib.pyplot as plt
import requests_async
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


async def getUrlTitleAsync(url):
    resp = await requests_async.get(url)
    title = str(
        BeautifulSoup(resp.text, 'html.parser').find('title')
    )
    return title


async def async_main(urls):
    titles = [getUrlTitleAsync(u) for u in urls]
    return await asyncio.gather(*titles)


@time_decorator
def getAsync(urls):
    return asyncio.run(async_main(urls))


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


def plot(num_processes, run_times):
    plt.scatter(num_processes, run_times)
    plt.title("[bradlet2] getMulti Runtimes on fetched URL list")
    plt.xlabel("Number of Processes")
    plt.ylabel("Retrieval Time")
    plt.show()


# Added this so that I could run in PyCharm w/ the play button.
if __name__ == '__main__':
    fetch_urls = True

    if fetch_urls:
        urls = requests \
                   .get('https://thefengs.com/wuchang/courses/cs495/urls.txt') \
                   .text \
                   .split('\n')[:39]
    else:
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

    run_multi = False
    run_async = True

    if run_multi:
        parallelization = [40, 30, 20, 10, 5, 2]
        results = [getMulti(urls, n) for n in parallelization]
        plot(parallelization, results)
        outputs = [f'[N={n}] getMulti time: {time:0.2f}' for n, time in zip(parallelization, results)]
        print(outputs)
    elif run_async:
        print(f'Async version: {getAsync(urls):0.2f}')
    else:
        print(f'{getSequential(urls):0.2f}')
