"""In this file tests for `run` scripts are gathered."""
import subprocess


class TestRun:
    """Run class unit tests."""

    def test_running_without_url(self):
        """Test running script without passing url."""
        args = ["python", "run.py"]
        sb = subprocess.call(args)
        assert sb == 1

    def test_running_with_url(self):
        """Test running script with url."""
        args = ["python", "run.py", "www.test.com"]
        sb = subprocess.call(args)
        assert sb == 0
