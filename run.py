"""
Main script that generates site map starting from web page
provided as parameter.

Usage:
    run.py <url>
    run.py <url> [--limit=<int>]

Options:
    -h, --help          Show this screen
    --version           Show version
    --limit=<int>       Max number of gathered links [default: 10].
"""
from docopt import docopt
from pprint import pprint

from crawler import Crawler

if __name__ == '__main__':
    arguments = docopt(__doc__, version='siteMapGen v0.1')
    crawler = Crawler(arguments.get('<url>'), int(arguments.get('--limit')))
    crawler.analyze()
    pprint(crawler.links)
