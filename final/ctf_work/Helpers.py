import sys


# Pull site info from cli args -- drop https:// if included
def parseArgsForSite():
    try:
        s = sys.argv[1]
        if 'https://' in s:
            s = s.rstrip('/').lstrip('https://')
        return s
    except IndexError:
        raise IndexError("Need to provide site URL when running script")
