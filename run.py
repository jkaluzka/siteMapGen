"""Main script that generates site map starting from web page provided as parameter.

Usage:
    run.py <url>
    run.py <url> [--limit=<int>]
    run.py <url> [--ext=<str>]
    run.py <url> [--output-file=<file_name>]
    run.py <url> [--limit=<int>] [--ext=<str>]
    run.py <url> [--limit=<int>] [--output-file=<file_name>]
    run.py <url> [--ext=<str>] [--output-file=<file_name>]
    run.py <url> [--limit=<int>] [--ext=<str>] [--output-file=<file_name>]

Options:
    -h, --help                  Show this screen
    --version                   Show version
    --limit=<int>               Max number of gathered links [default: 10]
    --ext=<str>                 Output extension: csv or xml [default: xml]
    --output-file=<file_name>   Output file name [default: output]
"""
from docopt import docopt

from crawler import Crawler
from writer import WriterManager

if __name__ == '__main__':
    arguments = docopt(__doc__, version='siteMapGen v0.1')
    crawler = Crawler(arguments.get('<url>'), int(arguments.get('--limit')))
    crawler.analyze()

    output_file = arguments.get('--output-file')
    extension = arguments.get('--ext')
    if not output_file.endswith(extension):
        # update output file with requested extensions
        output_file = '{}.{}'.format(output_file, extension)

    manager = WriterManager(output_file)
    manager.export_data(crawler.links)
