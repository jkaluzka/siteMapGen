"""Script contains crawler class."""
import requests
import logging

from urllib import parse
from bs4 import BeautifulSoup

logging.basicConfig()
_logger = logging.getLogger(__name__)


class Crawler:
    """
    Crawler class responsible for searching links on web page.
    """

    def __init__(self, base_url, limit=10):
        """
        :param base_url: str - web page url
        :param limit: int - limit number of links that should be gathered
        """
        if not base_url:
            raise AttributeError('Wrong base_url: %s' % base_url)

        if not base_url.startswith('http'):
            base_url = 'http://{}'.format(base_url)
        self.base_url = base_url
        self.server = parse.urlsplit(base_url)[1]
        self.limit = limit

        self.pages = {base_url, }
        self.links = set()

    def _join_url(self, url):
        """
        Helper method for removing any existing fragment
        of URL. Finally prepend `url` with `base_url`
        
        :param url: str - url to check
        :return: str - url with prepended `base_url`
        """
        _url, _ = parse.urldefrag(url)
        return parse.urljoin(self.base_url, _url)

    def analyze(self):
        """
        Method analyze web page looking for links that are not
        links to mail, or lead to outer pages.
        """
        while self.pages and self.limit:
            page = self.pages.pop()
            if page in self.links:
                # page already visited, we can skip it
                continue

            resp = requests.get(page)

            if resp.status_code >= 400:
                _logger.debug('page {} not accessible with error: {}'.format(
                    page, resp.status_code))
                continue

            if 'text/html' not in resp.headers.get('Content-Type'):
                # skip everything what is not an HTML page
                continue

            # add page to links and decrease limit
            self.links.add(page)
            self.limit -= 1
            soup = BeautifulSoup(resp.content, 'html.parser')

            for link in soup.find_all('a'):
                value = link.get('href')
                if not value:
                    # skip link without `href`
                    continue

                is_internal = (
                    value.startswith('/') or
                    parse.urlsplit(value).netloc == self.server
                    and 'mailto:' not in value
                )
                if is_internal:
                    # only internal links should be analyzed later
                    self.pages.add(self._join_url(value))



