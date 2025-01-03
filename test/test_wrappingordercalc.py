import subprocess
import sys
import tempfile

from os import path as ospath
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

sys.path.append(ospath.abspath('../'))

from src.wrappingordercalc import main, parse_arguments, ReturnCode


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
@patch.object(Path, 'open', mock_open(read_data='2x3x4'))
def test_main_happy_path_single_line(mock_is_file, mock_exists, capsys):
    mock_args = ['script_name', 'valid_file.txt']
    with patch('sys.argv', mock_args):
        result = main()
    captured = capsys.readouterr()

    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    assert 'Total Square Feet of Wrapping Paper: 58' in captured.out
    assert captured.err == ''
    assert result == ReturnCode.SUCCESS


@pytest.mark.component
@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', mock_open(read_data='2x3x4\n1x1x10\n'))
def test_main_happy_path_more_lines(mock_is_file, mock_exists, capsys):
    mock_args = ['script_name', 'valid_file.txt']
    with patch('sys.argv', mock_args):
        result = main()
    captured = capsys.readouterr()

    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    assert 'Total Square Feet of Wrapping Paper: 101' in captured.out
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
@patch.object(Path, 'open', mock_open(read_data='1x1x1\n1xx2x3'))
def test_main_malformed_file(mock_is_file, mock_exists, capsys):
    mock_args = ['script_name', 'malformed_file.txt']
    with patch('sys.argv', mock_args):
        result = main()
    captured = capsys.readouterr()

    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    assert captured.out == ''
    assert (
        'Malformed dimensions file sequence, please verify'
        ' that it contains only lines in the format: "<length>x<width>x<height>"'
        in captured.err
    )
    assert result == ReturnCode.MALFORMED_INPUT_ERROR


# integration tests
@pytest.mark.integration
def test_main_block_success():
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write('1x1x1\n1x1x1')
        temp_file_path = temp_file.name

    result = subprocess.run(
        [sys.executable, '../src/wrappingordercalc.py', temp_file_path],
        text=True,
        capture_output=True
    )

    assert result.returncode == 0
    assert 'Total Square Feet of Wrapping Paper: 14' in result.stdout
    assert result.stderr == ''
