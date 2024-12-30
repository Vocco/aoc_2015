import time

from os import path as ospath
from sys import path as syspath

import pytest

syspath.append(ospath.abspath('../'))

from src.floordirections import FloorDirectionsAnalysis, InvalidFloorDirectionsError


# unit tests
def test_analysis_happy_path():
    analysis = FloorDirectionsAnalysis('((())')
    assert analysis.final_floor == 1

    analysis = FloorDirectionsAnalysis('(()(()(')
    assert analysis.final_floor == 3

    analysis = FloorDirectionsAnalysis('))(((((')
    assert analysis.final_floor == 3

    analysis = FloorDirectionsAnalysis('())')
    assert analysis.final_floor == -1

    analysis = FloorDirectionsAnalysis('))(')
    assert analysis.final_floor == -1

    analysis = FloorDirectionsAnalysis(')())())')
    assert analysis.final_floor == -3


def test_analysis_malformed_sequence():
    with pytest.raises(InvalidFloorDirectionsError):
        analysis = FloorDirectionsAnalysis('(x()')


def test_analysis_empty_sequence():
    analysis = FloorDirectionsAnalysis('')
    assert analysis.final_floor == 0


def test_analysis_single_direction_sequence_opening():
    analysis = FloorDirectionsAnalysis('(')
    assert analysis.final_floor == 1


def test_analysis_single_direction_sequence_closing():
    analysis = FloorDirectionsAnalysis(')')
    assert analysis.final_floor == -1


def test_analysis_equal_number_of_opening_and_closing():
    analysis = FloorDirectionsAnalysis('()()')
    assert analysis.final_floor == 0


def test_analysis_only_opening_brackets():
    analysis = FloorDirectionsAnalysis('((((')
    assert analysis.final_floor == 4


def test_analysis_only_closing_brackets():
    analysis = FloorDirectionsAnalysis('))))')
    assert analysis.final_floor == -4


# performance tests
@pytest.mark.perf
def test_analysis_large_input():
    analysis = FloorDirectionsAnalysis(')' * 6_000_000 + '(' * 1_000_000)

    start = time.perf_counter()
    result = analysis.final_floor
    end = time.perf_counter()

    assert end - start < 1.0
    assert result == -5_000_000
