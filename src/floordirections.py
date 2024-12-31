# SPDX-License-Identifier: MIT
# Copyright (c) Vojtech Krajnansky
"""Capabilities for floor directions analysis.

This module computes the final floor and the first direction which leads to an underground floor
from a sequence of directions.

Valid directions are:
   - '(': meaning go up 1 floor.
   - ')': meaning go down 1 floor.

Constants:
    FloorDirectionsAnalysis.VALID_DIRECTIONS: The set of valid floor directions.

Classes:
    FloorDirectionsAnalysis: Handles direction sequence validation and computes:
        - The final floor.
        - The position of the first direction leading to basement (indexed from 1).

Exceptions:
    FloorDirectionsAnalysisError: The base exception for this module.
    InvalidFloorDirectionsError: A sequence is not a valid direction sequence.

Example:
    >>> # analyze a directions sequence:
    >>> from directions import FloorDirectionsAnalysis, FloorDirectionsAnalysisError
    >>> try:
    ...     analysis = FloorDirectionsAnalysis(directions_sequence)
    ...     print(f'Final Floor: {analysis.final_floor}')
    ...     print(f'First basement direction is at: {analysis.first_basement_direction_position}')
    ... except FloorDirectionsAnalysisError as e:
    ...     print(f'An error occurred: {e}')

Requirements:
    - Python >= 3.5

Author:
    Vojtech Krajnansky (https://github.com/Vocco)

License:
    This module is licensed under the MIT License. See the LICENSE file in the project root
    for full license text.
"""


# exceptions
class FloorDirectionsAnalysisError(ValueError):
    """Base exception for FloorDirectionsAnalysis."""


class InvalidFloorDirectionsError(FloorDirectionsAnalysisError):
    """An invalid character was encountered in a directions sequence."""


# classes
class FloorDirectionsAnalysis:
    """Analyzes sequences of floor directions.

    Args:
        sequence (str): The sequence of directions to analyze.

    Attributes:
        VALID_DIRECTIONS (set(str)): Allowed direction characters ('(', ')').
        final_floor (int): The computed final floor.
        first_basement_direction_position (int): The computed position of the first direction
            leading to a basement floor, indexed from 1. If no such position is found, this is 0.

    Methods:
        is_valid_directions_sequence(sequence): Check if the sequence contains
            only valid floor directions.

    Example:
        >>> # get valid instructions:
        >>> FloorDirectionsAnalysis.VALID_DIRECTIONS
        {'(', ')'}
        >>> # check if a sequence is a valid directions sequence:
        >>> FloorDirectionsAnalysis.is_valid_directions_sequence('(')
        True
        >>> # analyze a directions sequence:
        >>> analysis = FloorDirectionsAnalysis('((())')
        >>> analysis.final_floor
        1
        >>> analysis.first_basement_direction_position
        0
        >>> analysis = FloorDirectionsAnalysis('())((((')
        >>> analysis.final_floor
        3
        >>> analysis.first_basement_direction_position
        2
        >>> # empty instructions behavior:
        >>> FloorDirectionsAnalysis('').final_floor
        0
        >>> FloorDirectionsAnalysis('').first_basement_direction_position
        0

    Raises:
        InvalidFloorDirectionsError: If the provided sequence contains invalid characters.
    """
    VALID_DIRECTIONS = {'(', ')'}

    def __init__(self, sequence: str) -> None:
        """Initialize a FloorDirectionsAnalysis instance.
        
        Args:
            sequence (str): The directions sequence to analyze.

        Raises:
            InvalidFloorDirectionsError: If `sequence` contains invalid characters.
        """
        self._directions = self._validate_directions_sequence(sequence)
        self._final_floor = None
        self._first_basement_direction_position = None

    @staticmethod
    def _validate_directions_sequence(sequence: str) -> str:
        """Validate that the sequence contains only valid directions.

        Returns:
            str: The validated sequence.

        Raises:
            InvalidFloorDirectionsError: If `sequence` contains invalid characters.
        """
        if not FloorDirectionsAnalysis.is_valid_directions_sequence(sequence):
            raise InvalidFloorDirectionsError(
                'Sequence contains invalid characters; only "(" and ")" are allowed')
        return sequence

    @staticmethod
    def is_valid_directions_sequence(sequence: str) -> bool:
        """Check if the sequence contains only valid floor directions.
        
        Example:
            >>> FloorDirectionsAnalysis.is_valid_directions_sequence('(')
            True
            >>> FloorDirectionsAnalysis.is_valid_directions_sequence('(x(')
            False
            >>> FloorDirectionsAnalysis.is_valid_directions_sequence('')
            True
        """
        return all(char in FloorDirectionsAnalysis.VALID_DIRECTIONS for char in sequence)

    def _compute_final_floor(self) -> int:
        """Return the final based on the directions sequence."""
        return sum(1 if char == '(' else -1 for char in self._directions)

    def _find_first_basement_direction(self) -> int:
        """Return the position of the first direction which leads to a basement floor."""
        current_floor = 0

        for position, direction in enumerate(self._directions, start=1):
            current_floor += 1 if direction == '(' else -1
            if current_floor == -1:
                return position

        return 0

    @property
    def final_floor(self) -> int:
        """Return the final floor number."""
        if self._final_floor is None:
            self._final_floor = self._compute_final_floor()
        return self._final_floor

    @property
    def first_basement_direction_position(self) -> int:
        """Return the first direction leading to a basement floor."""
        if self._first_basement_direction_position is None:
            self._first_basement_direction_position = self._find_first_basement_direction()
        return self._first_basement_direction_position
