# SPDX-License-Identifier: MIT
# Copyright (c) Vojtech Krajnansky
"""File reading utilities.

This module provides functions and exceptions for safe reading of file contents
with enhanced error handling.

Functions:
    - read_file(file_path): Returns the contents of a file at the given path.
    - read_lines(file_path): Returns a list of lines from a file at the given path.

Exceptions:
    - FileInputError: The base exception for this module.
    - PathDoesNotExistError: The provided path does not exist.
    - NotAFileError: The path points to a non-file resource.
    - NotAccessibleError: The file cannot be accessed.
    - FileEncodingError: The file has unexpected encoding.

Type Definitions:
    - PathType: Union of `str` and `os.PathLike`.

Example:
    >>> # read file contents:
    >>> from fileinput import FileInputError, read_file, read_lines
    >>> try:
    ...     content = read_file('example.txt')
    ...     print(content)
    ... except FileInputError as e:
    ...     print(f'An error occurred: {e}')
    >>> # read lines from a file:
    >>> try:
    ...     lines = read_lines('example.txt')
    ... except FileInputError as e:
    ...     print(f'An error occurred: {e}')
    ...
    >>> for line in lines:
    ...     print(line)

Requirements:
    - Python >= 3.10

Author:
    Vojtech Krajnansky (https://github.com/Vocco)

License:
    This module is licensed under the MIT License. See the LICENSE file in the project root
    for full license text.
"""
from os import PathLike
from pathlib import Path


# type definitions
PathType = str | PathLike


# exceptions
class FileInputError(Exception):
    """Base exception for `fileinputhandler` errors."""


class FileEncodingError(FileInputError):
    """A file has unexpected encoding."""


class NotAccessibleError(FileInputError):
    """A file cannot be accessed."""


class NotAFileError(FileInputError):
    """A specified path does not point to a file."""


class PathDoesNotExistError(FileInputError):
    """A specified path does not exist."""


# functions
def read_file(file_path: PathType) -> str:
    """Return the text content of a UTF-8 encoded file.

    Args:
        file_path (PathType): The path to the file to be read.

    Raises:
        PathDoesNotExistError: If `file_path` does not exist in the file system.
        NotAFileError: If `file_path` does not point to a file.
        NotAccessibleError: If the file at `file_path` cannot be read.
        FileEncodingError: If the file at `file_path` is not UTF-8 encoded.

    Example:
        >>> try:
        ...     content = read_file('example.txt')
        ...     print(content)
        ... except FileInputError as e:
        ...     print(f'An error occurred: {e}')
    """
    path = Path(file_path)

    if not path.exists():
        raise PathDoesNotExistError(f'The resource "{path}" does not exist')

    if not path.is_file():
        raise NotAFileError(f'The resource "{path}" is not a file')

    try:
        with path.open('r', encoding='utf-8') as file:
            return file.read()
    except PermissionError as error:
        raise NotAccessibleError(f'The file "{path}" is not accessible') from error
    except UnicodeDecodeError as error:
        raise FileEncodingError(f'The file "{path}" is not UTF-8 encoded') from error


def read_lines(file_path: PathType) -> list[str]:
    """Return the lines of a UTF-8 encoded file.

    Args:
        file_path (PathType): The path to the file from which to read lines.

    Raises:
        PathDoesNotExistError: If `file_path` does not exist in the file system.
        NotAFileError: If `file_path` does not point to a file.
        NotAccessibleError: If the file at `file_path` cannot be read.
        FileEncodingError: If the file at `file_path` is not UTF-8 encoded.

    Example:
        >>> try:
        ...     lines = read_lines('example.txt')
        ... except FileInputError as e:
        ...     print(f'An error occurred: {e}')
        ...
        >>> for line in lines:
        ...     print(line)
    """
    path = Path(file_path)

    if not path.exists():
        raise PathDoesNotExistError(f'The resource "{path}" does not exist')

    if not path.is_file():
        raise NotAFileError(f'The resource "{path}" is not a file')

    try:
        with path.open('r', encoding='utf-8') as file:
            return file.readlines()
    except PermissionError as error:
        raise NotAccessibleError(f'The file "{path}" is not accessible') from error
    except UnicodeDecodeError as error:
        raise FileEncodingError(f'The file "{path}" is not UTF-8 encoded') from error
