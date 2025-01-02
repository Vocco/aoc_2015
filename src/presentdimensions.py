# SPDX-License-Identifier: MIT
# Copyright (c) Vojtech Krajnansky
"""Dimensional attributes of Christmas presents.

This module manages the dimensions of presents modeled as perfect right rectangular prisms.

Classes:
    PresentDimensions: Holds dimensional attributes of a Christmas present.

Exceptions:
    PresentDimensionsError: The base exception for this module.
    PresentDimensionsNotPositiveError: A non-positive dimension was encountered.
    InvalidPresentRepresentationError: A string representation of present dimensions is malformed.

Example:
    >>> # get the surface area of a present:
    >>> from presentdimensions import PresentDimensions, PresentDimensionsError
    >>> try:
    ...     present_dims = PresentDimensions(length, width, height)
    ...     print(f'Surface area: {present_dims.surface_area}')
    ... except PresentDimensionsError as e:
    ...     print(f'An error occurred: {e}')
    >>> # instantiate from a string representation and get side areas:
    >>> try:
    ...     present_dims = PresentDimensions.from_string(dimension_representation)
    ...     print(f'Side areas sorted from smallest to largest: {present_dims.side_areas}')
    ...     print(f'Smallest side area: {present_dims.smallest_side_area}')
    ... except PresentDimensionsError as e:
    ...     print(f'An error occurred: {e}')

Requirements:
    - Python >= 3.6

Author:
    Vojtech Krajnansky (https://github.com/Vocco)

License:
    This module is licensed under the MIT License. See the LICENSE file in the project root
    for full license text.
"""


# exceptions
class PresentDimensionsError(ValueError):
    """Base exception for `PresentDimensions`."""


class InvalidPresentRepresentationError(PresentDimensionsError):
    """A string representation of a present's dimensions has invalid format."""


class PresentDimensionsNotPositiveError(PresentDimensionsError):
    """A non-positive dimension was encountered."""


# classes
class PresentDimensions:
    """Represents the dimensions of a Christmas present (a perfect right rectangular prism).

    Args:
        length (int): The length of the present.
        width (int): The width of the present.
        height (int): The height of the present.

    Attributes:
        side_areas (list[int]): Areas of the present's sides, sorted from smallest to largest.
        smallest_side_area (int): The area of the present's smallest side.
        surface_area (int): The total surface area of the present.
        height (int): The height of the present.
        length (int): The length of the present.
        width (int): The width of the present.

    Methods:
        from_string(representation): Instantiate a PresentDimensions object
            from a string representation of dimensions.

    Example:
        >>> # get the areas of a present
        >>> present_dims = PresentDimensions(3, 2, 1)
        >>> present_dims.side_areas
        [2, 3, 6]
        >>> present_dims.surface_area
        22
        >>> present_dims.smallest_side_area
        2
        >>> # instantiate dimensions from a string representation
        >>> present_dims = PresentDimensions.from_string('3x2x1')

    Raises:
        PresentDimensionsNotPositiveError: If `length`, `width`, or `height` is not positive.
        InvalidPresentRepresentationError: If a string representation of the present's dimensions
            is malformed.
    """
    def __init__(self, length: int, width: int, height: int) -> None:
        """Initialize a Present instance, ensuring dimensions are positive integers.
        
        Raises:
            PresentDimensionsNotPositiveError: If `length`, `width`, or `height` is not positive.
        """
        if not (isinstance(length, int) and isinstance(width, int) and isinstance(height, int)):
            raise TypeError(
                'All dimensions must be integers, but got:'
                f' {type(length).__name__}, {type(width).__name__}, {type(height).__name__}'
            )
        if length < 1 or width < 1 or height < 1:
            raise PresentDimensionsNotPositiveError(
                f'Dimensions must be positive, but got: {length}, {width}, {height}')

        self._length = length
        self._width = width
        self._height = height
        self._side_areas = sorted((length * width, length * height, width * height))
        self._surface_area = 2 * sum(self._side_areas)

    @classmethod
    def from_string(cls, representation: str) -> None:
        """Initialize a PresentDimensions instance from a string dimensions representation.
        
        Dimensions are expected to be in the format:
            <length>x<width>x<height>
        
        Where each dimension is a positive integer.
        
        Raises:
            PresentDimensionsNotPositiveError: If any of the dimensions is not positive.
            InvalidPresentRepresentationError: If `representation` is malformed.
        """
        try:
            dimensions = [int(dimension) for dimension in representation.strip().split('x')]

            if len(dimensions) != 3:
                raise ValueError(f'Expected 3 dimensions, but got: {len(dimensions)}')

            return cls(*dimensions)
        except AttributeError as error:
            raise TypeError(
                'Present representation must be a string, but got:'
                f' {type(representation).__name__}'
            ) from error
        except ValueError as error:
            raise InvalidPresentRepresentationError(
                'Present representation must have the format "<length>x<width>x<height>",'
                f' but got: {representation}'
            ) from error

    @property
    def height(self) -> int:
        """Return the height of the present."""
        return self._height

    @property
    def length(self) -> int:
        """Return the length of the present."""
        return self._length

    @property
    def width(self) -> int:
        """Return the width of the present."""
        return self._width

    @property
    def side_areas(self) -> list[int]:
        """Return the areas of the present's sides sorted from smallest to largest."""
        return self._side_areas

    @property
    def smallest_side_area(self) -> int:
        """Return the area of the present's smallest side."""
        return self._side_areas[0]

    @property
    def surface_area(self) -> int:
        """Return the surface area of the present."""
        return self._surface_area
