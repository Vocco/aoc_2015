# SPDX-License-Identifier: MIT
# Copyright (c) Vojtech Krajnansky
"""Santa's floor direction helper.

This module computes the final floor based on a sequence of directions from a file.
Solution for Advent of Code 2015 Day 01, Part 1.

Usage:
    Provide a valid directions file (containing only "(" and ")" characters in a single line).
    Run the program as:
        python floorfinder.py FILE

Constants:
    ReturnCode.SUCCESS: Indicates successful execution.
    ReturnCode.KEYBOARD_INTERRUPT: Indicates the execution was interrupted.
    ReturnCode.UNEXPECTED_ERROR: Indicates that an unexpected error has occurred.
    ReturnCode.FILE_READING_ERROR: Indicates that the input file could not be read.
    ReturnCode.MALFORMED_INPUT_ERROR: Indicates that the contents of the input file are malformed.

Classes:
    ReturnCode: Defines return codes for program execution.

Functions:
    parse_arguments: Parses and validates command-line arguments.
    main: Program entry point.

Requirements:
    - Python >= 3.10

Author:
    Vojtech Krajnansky (https://github.com/Vocco)

License:
    This program is licensed under the MIT License. See the LICENSE file in the project root
    for full license text.
"""
from argparse import ArgumentParser
from enum import IntEnum
from pathlib import Path
from sys import exit as sysexit


from floordirections import FloorDirectionsAnalysis, FloorDirectionsAnalysisError
from fileinputhandler import FileInputError, read_file
from outputhandler import notify_error, notify_success


# constants
class ReturnCode(IntEnum):
    """Return codes for program execution.
    
    Attributes:
        SUCCESS (0): Indicates successful execution.
        KEYBOARD_INTERRUPT (1): Indicates the execution was interrupted.
        UNEXPECTED_ERROR (2): Indicates that an unexpected error has occurred.
        FILE_READING_ERROR (3): Indicates that the input file could not be read.
        MALFORMED_INPUT_ERROR (4): Indicates that the input file contents are malformed.
    """
    SUCCESS = 0
    KEYBOARD_INTERRUPT = 1
    UNEXPECTED_ERROR = 2
    FILE_READING_ERROR = 3
    MALFORMED_INPUT_ERROR = 4


# functions
def parse_arguments() -> Path:
    """Parse command-line arguments to extract the input file path.

    Returns:
        pathlib.Path: Path to the input file provided as an argument.
    """
    parser = ArgumentParser(description='Compute the final floor from a directions file.')
    parser.add_argument(
        'file_path',
        metavar='FILE',
        type=Path,
        help='path to the directions file (must contain only "(" and ")" characters).'
    )
    return parser.parse_args().file_path


def main() -> int:
    """Main program entry point.
    
    Parses command-line arguments, reads the provided floor directions file,
    and computes the final floor to which the sequence leads.

    Returns:
        int: Exit code indicating execution status.
            - SUCCESS (0): Indicates successful execution.
            - FILE_READING_ERROR (3): Indicates that the input file could not be read.
            - MALFORMED_INPUT_ERROR (4): Indicates that the input file contents are malformed.

    Side Effects:
        - Upon success: Notifies the user about success and prints the final floor to `stdout`.
        - Upon failure: Notifies the user about the failure and prints the reason to `stderr`.
    """
    try:
        file_path = parse_arguments()
        file_content = read_file(file_path)
        analysis = FloorDirectionsAnalysis(file_content)
        notify_success(
            f'Final Floor: {analysis.final_floor}'
            f'\nFirst basement direction position: {analysis.first_basement_direction_position}'
        )
        return ReturnCode.SUCCESS
    except FileInputError as error:
        notify_error(
            'Could not read input file, please verify that you have provided the correct path'
            f'\nCause: {error}'
        )
        return ReturnCode.FILE_READING_ERROR
    except FloorDirectionsAnalysisError as error:
        notify_error(
            'Malformed directions sequence,'
            f' please verify that it contains only "(" and ")" characters\nCause: {error}'
        )
        return ReturnCode.MALFORMED_INPUT_ERROR


if __name__ == '__main__':
    try:
        sysexit(main())
    except KeyboardInterrupt:
        notify_error('Execution interrupted by user')
        sysexit(ReturnCode.KEYBOARD_INTERRUPT)
    except Exception as error:
        notify_error(f'Critical failure\nCause: {error}')
        sysexit(ReturnCode.UNEXPECTED_ERROR)
