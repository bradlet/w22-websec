import requests

site = 'ac241fca1ea763a5c06421990079006f.web-security-academy.net'
s = requests.Session()


def checkValidHtmlTags():
    tag_file = open('validHtmlTags.txt', 'r')
    tags = tag_file.readlines()

    for tag in tags:
        search_url = f'https://{site}/?search=<{tag.strip()}>'  # Remove any leading/trailing whitespace from file IO
        resp = s.get(search_url)
        if resp.status_code == 200:
            print(f'Success: {tag} gives code {resp.status_code}')
        else:
            print(f'Error: {tag} gives response: {resp.text}')


def checkValidEvents():
    event_file = open('validEvents.txt', 'r')
    events = event_file.readlines()
    for event in events:
        search_url = f'https://{site}/?search=<animatetransform {event.strip()}>'
        resp = s.get(search_url)
        if resp.status_code == 200:
            print(f'Success: {event.strip()} gives code {resp.status_code}')


if __name__ == '__main__':
    # checkValidHtmlTags()
    checkValidEvents()

    # tag = '''<svg>'''
    # search_url = f'https://{site}/?search=<{tag}>'
    # resp = s.get(search_url)
    # print(f'Status code is {resp.status_code} with response text {resp.text}')
