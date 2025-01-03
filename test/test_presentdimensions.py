from os import path as ospath
from sys import path as syspath

import pytest

syspath.append(ospath.abspath('../'))

from presentdimensions import (
    InvalidPresentRepresentationError, PresentDimensions, PresentDimensionsNotPositiveError
)


def test_present_dimensions_dimensions_attributes():
    present = PresentDimensions(3, 2, 1)
    assert present.length == 3
    assert present.width == 2
    assert present.height == 1


def test_present_dimensions_side_areas():
    assert PresentDimensions(3, 2, 1).side_areas == [2, 3, 6]
    assert PresentDimensions(2, 2, 3).side_areas == [4, 6, 6]
    assert PresentDimensions(4, 4, 4).side_areas == [16, 16, 16]


def test_present_dimensions_smallest_side_area():
    assert PresentDimensions(3, 2, 1).smallest_side_area == 2
    assert PresentDimensions(2, 2, 3).smallest_side_area == 4
    assert PresentDimensions(4, 4, 4).smallest_side_area == 16


def test_present_dimensions_surface_area():
    assert PresentDimensions(3, 2, 1).surface_area == 22
    assert PresentDimensions(2, 2, 3).surface_area == 32
    assert PresentDimensions(4, 4, 4).surface_area == 96


def test_present_dimensions_negative_dimensions():
    with pytest.raises(PresentDimensionsNotPositiveError):
        PresentDimensions(-1, 2, 3)
    with pytest.raises(PresentDimensionsNotPositiveError):
        PresentDimensions(1, -2, 3)
    with pytest.raises(PresentDimensionsNotPositiveError):
        PresentDimensions(1, 2, -3)


def test_present_dimensions_type_error():
    with pytest.raises(TypeError):
        PresentDimensions('1', 2, 3)
    with pytest.raises(TypeError):
        PresentDimensions(1, '2', 3)
    with pytest.raises(TypeError):
        PresentDimensions(1, 2, '3')


def test_present_dimensions_from_string_happy_path():
    present = PresentDimensions.from_string('3x2x1')
    assert present.length == 3
    assert present.width == 2
    assert present.height == 1


@pytest.mark.parametrize(
    'input_string', [
    '',
    '3x2',
    '3x2x1x4',
    '3x2xabc',
    '3xx2',
    '3xx2x3',
    'x2x3',
    '2x3x',
    '3x2x-1',
    '3x-2x1',
    '-3x2x1'
])
def test_present_dimensions_from_string_malformed_string(input_string):
    with pytest.raises(InvalidPresentRepresentationError):
        PresentDimensions.from_string(input_string)


def test_present_dimensions_from_string_type_error():
    with pytest.raises(TypeError):
        PresentDimensions.from_string({'a': 2})
