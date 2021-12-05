"""The tests to run in this project.
To run the tests type,
$ nosetests --verbose
"""

from nose.tools import assert_true

BASE_URL = "http://localhost:5000"


def test_always_true():
    assert_true(True)
