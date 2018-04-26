"""In this file tests for Crawler scripts are gathered."""
import pytest

from crawler import Crawler


class TestCrawler:
    """Crawler class unit tests."""

    @pytest.mark.parametrize('url,expected,server_name', [
        ('www.test.com', 'http://www.test.com', 'www.test.com'),
        ('http://www.test.com', 'http://www.test.com', 'www.test.com'),
        ('https://www.test.com', 'https://www.test.com', 'www.test.com'),
        ('https://www.test.co.uk', 'https://www.test.co.uk', 'www.test.co.uk'),
    ])
    def test_extract_url_properly(self, url, expected, server_name):
        """Test Crawler can extract url properly"""
        crawler = Crawler(url)
        assert crawler.base_url == expected
        assert crawler.server == server_name

    def test_raise_exception_when_no_url(self):
        """Test Crawler raises exception when no url were passed."""
        with pytest.raises(AttributeError):
            Crawler(None)

    @pytest.mark.usefixtures('mocker', 'correct_response')
    def test_analyzing_page_different_style(self, mocker, correct_response):
        """Test getting links from page content."""
        requests_mck = mocker.patch('requests.get')
        requests_mck.return_value = correct_response

        url = 'test1.com'
        crawler = Crawler(url)
        crawler.analyze()

        expected = {
            'http://test1.com',
            'http://test1.com/help.html',
        }
        assert crawler.links == expected

    @pytest.mark.usefixtures('mocker', 'correct_response')
    def test_crawling_over_page_with_limit(self, mocker, correct_response):
        """Test that crawling will stop when limit value were met."""
        requests_mck = mocker.patch('requests.get')
        requests_mck.return_value = correct_response

        url = 'test1.com'
        crawler = Crawler(url, 1)
        crawler.analyze()

        expected = {'http://test1.com'}
        assert crawler.links == expected

    @pytest.mark.usefixtures('mocker', 'response_with_mail', 'not_found_response')
    def test_analyzing_page_with_mailto(self, mocker, response_with_mail, not_found_response):
        requests_mck = mocker.patch('requests.get')
        requests_mck.side_effect = [response_with_mail, not_found_response]

        url = 'test2.com'
        crawler = Crawler(url)
        crawler.analyze()

        # http://test2.com/help.html doesn't exists
        # that's why only base page is visible
        expected = {'http://test2.com'}
        assert crawler.links == expected
