import time

from os import path as ospath
from sys import path as syspath

import pytest

syspath.append(ospath.abspath('../'))

from src.floordirections import FloorDirectionsAnalysis, InvalidFloorDirectionsError


# unit tests
@pytest.mark.parametrize(
    'input_sequence, expected_floor', [
    ('((())', 1),
    ('(()(()(', 3),
    ('))(((((', 3),
    ('())', -1),
    ('))(', -1),
    (')())())', -3),
    ('', 0),
    ('(', 1),
    (')', -1),
    ('()()', 0),
    ('((((', 4),
    ('))))', -4)
])
def test_analysis_final_floor(input_sequence, expected_floor):
    analysis = FloorDirectionsAnalysis(input_sequence)
    assert analysis.final_floor == expected_floor


@pytest.mark.parametrize(
    'input_sequence, expected_position', [
    (')', 1),
    ('()())', 5),
    ('', 0),
    ('(', 0),
    ('(((())()))(((', 0),
    ('(((())())))', 11)
])
def test_analysis_first_basement_direction_position(input_sequence, expected_position):
    analysis = FloorDirectionsAnalysis(input_sequence)
    assert analysis.first_basement_direction_position == expected_position


def test_analysis_malformed_sequence():
    with pytest.raises(InvalidFloorDirectionsError):
        FloorDirectionsAnalysis('(x()')


# performance tests
@pytest.mark.perf
def test_analysis_large_input():
    analysis = FloorDirectionsAnalysis(')' * 6_000_000 + '(' * 1_000_000)

    start = time.perf_counter()
    result = analysis.final_floor
    end = time.perf_counter()

    assert end - start < 1.0
    assert result == -5_000_000
