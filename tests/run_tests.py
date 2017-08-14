"""
In this file tests for `run` scripts are gathered.
"""
import subprocess
import unittest


class RunTest(unittest.TestCase):

    def test_running_without_url(self):
        args = ["python", "../run.py"]
        sb = subprocess.call(args)
        self.assertEqual(sb, 1)

    def test_running_with_url(self):
        args = ["python", "../run.py", "www.test.com"]
        sb = subprocess.call(args)
        self.assertEqual(sb, 0)


if __name__ == '__main__':
    unittest.main()
