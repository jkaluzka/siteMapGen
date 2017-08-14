"""
In this file tests for Crawler scripts are gathered.
"""
import unittest

import mock
from parameterized import parameterized

from crawler import Crawler


def mocked_responses(*args, **kwargs):
    class MockResponse:
        def __init__(self, body, status_code, headers):
            self.body = body
            self.content = body
            self.status_code = status_code
            self.headers = headers

        def read(self):
            return self.body

    _body = ''
    code = 404
    _headers = {'Content-Type': 'text/html'}
    if args[0] == 'http://test1.com':
        code = 200
        _body = '''
        <a href="/help.html#123">help</a>
        <a href="test1.com/help.html">help2</a>'
        '''
    if args[0] == 'http://test1.com/help.html':
        code = 200
        _body = '''help'''
    if args[0] == 'http://test2.com':
        code = 200
        _body = '''
        <a href="/help.html#123">help</a>
        <a href="mailto:help@test2.com">help2</a>
        '''
    return MockResponse(_body, code, _headers)


class CrawlerTest(unittest.TestCase):

    @parameterized.expand([
        ('www.test.com', 'http://www.test.com', 'www.test.com'),
        ('http://www.test.com', 'http://www.test.com', 'www.test.com'),
        ('https://www.test.com', 'https://www.test.com', 'www.test.com'),
    ])
    def test_url(self, url, expected, server_name):
        crawler = Crawler(url)
        self.assertEqual(crawler.base_url, expected)
        self.assertEqual(crawler.server, server_name)

    def test_raise_exception_when_no_url(self):
        with self.assertRaises(AttributeError):
            crawler = Crawler(None)
            self.assertEqual(crawler.base_url, None)

    @mock.patch('requests.get', side_effect=mocked_responses)
    def test_analyzing_page_different_style(self, mocked_resp):
        url = 'test1.com'
        crawler = Crawler(url)
        crawler.analyze()
        expected = [
            'http://test1.com',
            'http://test1.com/help.html',
        ]
        self.assertItemsEqual(crawler.links, expected)

    @mock.patch('requests.get', side_effect=mocked_responses)
    def test_crawling_over_page_with_limit(self, mocked_resp):
        url = 'test1.com'
        crawler = Crawler(url, 1)
        crawler.analyze()
        expected = ['http://test1.com']
        self.assertItemsEqual(crawler.links, expected)

    @mock.patch('requests.get', side_effect=mocked_responses)
    def test_analyzing_page_with_mailto(self, mocked_resp):
        url = 'test2.com'
        crawler = Crawler(url)
        crawler.analyze()
        # http://test2.com/help.html doesn't exists
        # that's why only base page is visible
        expected = ['http://test2.com']
        self.assertItemsEqual(crawler.links, expected)


if __name__ == '__main__':
    unittest.main()
