from os import path as ospath
from sys import path as syspath

import pytest

syspath.append(ospath.abspath('../'))

from src.outputhandler import notify_error, notify_success


# unit tests
def test_notify_error(capsys):
    test_error = 'Something went wrong'
    notify_error(test_error)
    captured = capsys.readouterr()

    assert captured.out == ''
    assert captured.err == f'Execution failed\n{test_error}\n'


def test_notify_success(capsys):
    test_message = 'Result is: 1'
    notify_success(test_message)
    captured = capsys.readouterr()

    assert captured.out == f'Execution successful\n{test_message}\n'
    assert captured.err == ''
