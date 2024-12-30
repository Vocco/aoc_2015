import subprocess
import sys
import tempfile

from os import path as ospath
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

sys.path.append(ospath.abspath('../'))
sys.path.append(ospath.abspath('../src'))

from src.floorfinder import main, parse_arguments, ReturnCode


# unit tests
def test_parse_arguments_happy_path():
    mock_args = ['script_name', 'valid_file.txt']
    with patch('sys.argv', mock_args):
        result = parse_arguments()
        assert isinstance(result, Path)
        assert result == Path(mock_args[1])


def test_parse_arguments_missing_argument():
    with patch('sys.argv', ['script_name']), pytest.raises(SystemExit):
        parse_arguments()


def test_parse_arguments_help_message():
    with patch('sys.argv', ['script_name', '-h']):
        with pytest.raises(SystemExit) as excinfo:
            parse_arguments()
    assert excinfo.value.code == 0


# component tests
@pytest.mark.component
@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', mock_open(read_data='(()'))
def test_main_happy_path(mock_is_file, mock_exists, capsys):
    mock_args = ['script_name', 'valid_file.txt']
    with patch('sys.argv', mock_args):
        result = main()
    captured = capsys.readouterr()

    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    assert 'Final Floor: 1' in captured.out
    assert captured.err == ''
    assert result == ReturnCode.SUCCESS


@pytest.mark.component
@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=False)
def test_main_not_a_file(mock_is_file, mock_exists, capsys):
    mock_args = ['script_name', 'path/to/directory']
    with patch('sys.argv', mock_args):
        result = main()
    captured = capsys.readouterr()

    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    assert captured.out == ''
    assert (
        'Could not read input file, please verify that you have provided the correct path'
        in captured.err
    )
    assert result == ReturnCode.FILE_READING_ERROR


@pytest.mark.component
@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', mock_open(read_data='(()a'))
def test_main_malformed_file(mock_is_file, mock_exists, capsys):
    mock_args = ['script_name', 'path/to/directory']
    with patch('sys.argv', mock_args):
        result = main()
    captured = capsys.readouterr()

    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    assert captured.out == ''
    assert (
        'Malformed directions sequence, please verify that it contains only "(" and ")" characters'
        in captured.err
    )
    assert result == ReturnCode.MALFORMED_INPUT_ERROR


# integration tests
@pytest.mark.integration
def test_main_block_success():
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write('())')  # Write the mock file content
        temp_file_path = temp_file.name

    # Call the script using the temporary file as input
    result = subprocess.run(
        [sys.executable, '../src/floorfinder.py', temp_file_path],
        text=True,
        capture_output=True
    )

    assert result.returncode == 0
    assert 'Final Floor: -1' in result.stdout
    assert result.stderr == ''
