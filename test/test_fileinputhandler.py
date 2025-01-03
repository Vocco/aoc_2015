from os import path as ospath
from pathlib import Path
from sys import path as syspath
from unittest.mock import patch, mock_open

import pytest

syspath.append(ospath.abspath('../'))

from src.fileinputhandler import (
    FileEncodingError,
    PathDoesNotExistError,
    NotAccessibleError,
    NotAFileError,
    read_file,
    read_lines
)


# unit tests
@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
def test_read_file_happy_path(mock_is_file, mock_exists):
    mock_content = 'Hello, world!'

    with patch.object(Path, 'open', mock_open(read_data=mock_content)) as mock_path_open:
        assert read_file('mock_file.txt') == mock_content
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=False)
def test_read_file_file_does_not_exist(mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(PathDoesNotExistError, match=f'The resource "{mock_file_path}" does not exist'):
        read_file(mock_file_path)
    mock_exists.assert_called_once()


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=False)
def test_read_file_not_a_file(mock_is_file, mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(NotAFileError, match=f'The resource "{mock_file_path}" is not a file'):
        read_file(mock_file_path)
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', side_effect=PermissionError)
def test_read_file_no_read_permission(mock_path_open, mock_is_file, mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(NotAccessibleError, match=f'The file "{mock_file_path}" is not accessible'):
        read_file(mock_file_path)
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
def test_read_file_empty_file(mock_is_file, mock_exists):
    with patch.object(Path, 'open', mock_open(read_data='')) as mock_path_open:
        assert read_file('mock_file.txt') == ''
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'Invalid start byte'))
def test_read_file_bad_encoding(mock_path_open, mock_is_file, mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(FileEncodingError, match=f'The file "{mock_file_path}" is not UTF-8 encoded'):
        read_file(mock_file_path)
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
def test_read_lines_happy_path(mock_is_file, mock_exists):
    mock_content = 'Hello, world!\nline 2\nline 3'

    with patch.object(Path, 'open', mock_open(read_data=mock_content)) as mock_path_open:
        assert read_lines('mock_file.txt') == mock_content.splitlines()
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=False)
def test_read_lines_file_does_not_exist(mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(PathDoesNotExistError, match=f'The resource "{mock_file_path}" does not exist'):
        read_lines(mock_file_path)
    mock_exists.assert_called_once()


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=False)
def test_read_lines_not_a_file(mock_is_file, mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(NotAFileError, match=f'The resource "{mock_file_path}" is not a file'):
        read_lines(mock_file_path)
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', side_effect=PermissionError)
def test_read_lines_no_read_permission(mock_path_open, mock_is_file, mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(NotAccessibleError, match=f'The file "{mock_file_path}" is not accessible'):
        read_lines(mock_file_path)
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
@patch.object(Path, 'open', side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'Invalid start byte'))
def test_read_lines_bad_encoding(mock_path_open, mock_is_file, mock_exists):
    mock_file_path = 'mock_file.txt'

    with pytest.raises(FileEncodingError, match=f'The file "{mock_file_path}" is not UTF-8 encoded'):
        read_lines(mock_file_path)
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
def test_read_lines_empty_file(mock_is_file, mock_exists):
    with patch.object(Path, 'open', mock_open(read_data='')) as mock_path_open:
        assert read_lines('mock_file.txt') == []
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
def test_read_lines_single_line(mock_is_file, mock_exists):
    mock_content = 'first line\n'
    with patch.object(Path, 'open', mock_open(read_data=mock_content)) as mock_path_open:
        assert read_lines('mock_file.txt') == mock_content.splitlines()
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')


@patch.object(Path, 'exists', return_value=True)
@patch.object(Path, 'is_file', return_value=True)
def test_read_lines_single_line_no_newline(mock_is_file, mock_exists):
    mock_content = 'first line'
    with patch.object(Path, 'open', mock_open(read_data=mock_content)) as mock_path_open:
        assert read_lines('mock_file.txt') == [mock_content]
    mock_exists.assert_called_once()
    mock_is_file.assert_called_once()
    mock_path_open.assert_called_once_with('r', encoding='utf-8')
