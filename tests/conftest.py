"""Defines fixtures available to all tests."""
import pytest


class MockResponse:
    """Class for creating mock response objects."""

    def __init__(self, body, status_code, headers=None):
        if not headers:
            headers = {'Content-Type': 'text/html'}
        self.body = body
        self.content = body
        self.status_code = status_code
        self.headers = headers

    def read(self):
        return self.body


@pytest.fixture
def correct_response():
    """Returns correct response."""
    _body = '''
        <a href="/help.html#123">help</a>
        <a href="test1.com/help.html">help2</a>'
    '''
    return MockResponse(_body, 200)


@pytest.fixture
def response_with_mail():
    """Returns correct response containing mail link."""
    _body = '''
        <a href="/help.html#123">help</a>
        <a href="mailto:help@test2.com">help2</a>
    '''
    return MockResponse(_body, 200)


@pytest.fixture
def correct_empty_response():
    """Returns correct but without any link response."""
    _body = 'help'
    return MockResponse(_body, 200)


@pytest.fixture
def not_found_response():
    """Returns correct but without any link response."""
    _body = '404 Not Found'
    return MockResponse(_body, 404)
