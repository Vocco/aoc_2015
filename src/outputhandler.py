# SPDX-License-Identifier: MIT
# Copyright (c) Name Surname
"""Output handling utilities.

This module provides functions to notify the user of success or error messages
in a standardized format. Success messages are printed to `stdout`,
and error messages are printed to `stderr`.

Functions:
    notify_success(message): Notify the user about successful execution.
    notify_error(error): Notify the user about an execution error.

Example:
    >>> # notify about success:
    >>> notify_success('Result is: 1')
    Execution successful
    Result is: 1
    >>> # notify about error:
    >>> notify_error('Something went wrong')
    Execution failed
    Something went wrong

Requirements:
    - Python >= 3.5

Author:
    Name Surname (https://github.com/NameSurname)

License:
    This module is licensed under the MIT License. See the LICENSE file in the project root
    for full license text.
"""
from sys import stderr


# functions
def notify_error(error: str) -> None:
    """Print an error message to `stderr`.

    Informs the user that the execution has failed.

    Example:
        >>> notify_error('Something went wrong')
        Execution failed
        Something went wrong
    """
    print('Execution failed', file=stderr)
    print(error, file=stderr)


def notify_success(message: str) -> None:
    """Print a success message to `stdout`.
    
    Informs the user that the execution was successful.

    Example:
        >>> notify_success('Result is: 1')
        Execution successful
        Result is: 1
    """
    print('Execution successful')
    print(message)
