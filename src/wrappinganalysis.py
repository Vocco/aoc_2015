# SPDX-License-Identifier: MIT
# Copyright (c) Vojtech Krajnansky
"""Christmas present wrapping analysis capabilities.

This module computes the total amount of wrapping paper required to wrap a collection of presents.

Classes:
    WrappingAnalysis: Computes the total wrapping paper needed based on present dimensions.

Example:
    >>> # compute the amount of wrapping paper needed for a single present
    >>> from presentdimensions import PresentDimensions
    >>> from wrappinganalysis import WrappingAnalysis
    >>> WrappingAnalysis.wrapping_paper_required(PresentDimensions(1, 2, 3))
    24
    >>> # compute the total amount of wrapping paper needed for a list of presents
    >>> analysis = WrappingAnalysis(3 * [PresentDimensions(1, 2, 3)])
    >>> analysis.total_wrapping_paper_required
    72

Dependencies:
    presentdimensions

Requirements:
    - Python >= 3.9

Author:
    Vojtech Krajnansky (https://github.com/Vocco)

License:
    This module is licensed under the MIT License. See the LICENSE file in the project root
    for full license text.
"""


from presentdimensions import PresentDimensions


# classes
class WrappingAnalysis:
    """Computes wrapping paper requirements for a collection of presents.
    
    Args:
        present_dimensions_list (list[presentdimensions.PresentDimensions]):
            The dimensions of the presents to be wrapped.

    Attributes:
        total_wrapping_paper_required (int): Total wrapping paper area for all presents.

    Methods:
        wrapping_paper_required(present_dimensions): Calculates the amount of wrapping paper
            needed for a single present.

    Example:
        >>> # compute the amount of wrapping paper needed for a single present
        >>> from presentdimensions import PresentDimensions
        >>> from wrappinganalysis import WrappingAnalysis
        >>> WrappingAnalysis.wrapping_paper_required(PresentDimensions(1, 2, 3))
        24
        >>> # compute the total amount of wrapping paper needed for a list of presents
        >>> analysis = WrappingAnalysis(3 * [PresentDimensions(1, 2, 3)])
        >>> analysis.total_wrapping_paper_required
        72
        >>> WrappingAnalysis([]).total_wrapping_paper_required
        0
    """
    def __init__(self, present_dimensions_list: list[PresentDimensions]) -> None:
        """Initialize a `WrappingAnalysis` instance.
        
        Args:
            present_dimensions_list (list[presentdimensions.PresentDimensions]):
                The dimensions of the presents to be analyzed.
        """
        self._dims = self._validate_dimensions_list(present_dimensions_list)
        self._total_paper_area = -1

    @staticmethod
    def _compute_wrapping_paper_required(present_dimensions: PresentDimensions) -> int:
        """Compute the area of wrapping paper required to wrap a present of given dimensions."""
        return present_dimensions.surface_area + present_dimensions.smallest_side_area

    @staticmethod
    def _validate_present_dimensions(present_dimensions: PresentDimensions) -> PresentDimensions:
        """Validate that an object is a `PresentDimensions` instance.
        
        Returns:
            PresentDimensions: The validated object.

        Raises:
            TypeError: If `present_dimensions` is not an instance of `PresentDimensions`.
        """
        if not isinstance(present_dimensions, PresentDimensions):
            raise TypeError(
                'Expected a PresentDimensions instance, but got:'
                f' {type(present_dimensions).__name__}'
            )
        return present_dimensions

    @staticmethod
    def _validate_dimensions_list(dims_list: list[PresentDimensions]) -> list[PresentDimensions]:
        """Validate that an object is a list of `PresentDimensions` instances.
        
        Returns:
            list[PresentDimensions]: The validated list.

        Raises:
            TypeError: If `dims_list` is not a list of `PresentDimensions` instances.
        """
        if not isinstance(dims_list, list):
            raise TypeError(
                f'Present dimensions list must be a list, but got: {type(dims_list).__name__}')
        return [WrappingAnalysis._validate_present_dimensions(dims) for dims in dims_list]

    @staticmethod
    def wrapping_paper_required(present_dimensions: PresentDimensions) -> int:
        """Return the area of wrapping paper needed to wrap a present of given dimensions.
        
        Example:
            >>> from presentdimensions import PresentDimensions
            >>> from wrappinganalysis import WrappingAnalysis
            >>> WrappingAnalysis.wrapping_paper_required(PresentDimensions(1, 2, 3))
            24
        """
        return WrappingAnalysis._compute_wrapping_paper_required(
            WrappingAnalysis._validate_present_dimensions(present_dimensions))

    @property
    def total_wrapping_paper_required(self) -> int:
        """Return the total wrapping paper area needed to wrap all presents."""
        if self._total_paper_area < 0:
            self._total_paper_area = sum(map(self._compute_wrapping_paper_required, self._dims))
        return self._total_paper_area
