from os import path as ospath
from sys import path as syspath

import pytest

syspath.append(ospath.abspath('../'))

from src.floordirections import FloorDirectionsAnalysis, InvalidFloorDirectionsError


# unit tests
def test_analysis_happy_path():
    analysis = FloorDirectionsAnalysis('((())')
    analysis.analyze()
    assert analysis.final_floor == 1

    analysis = FloorDirectionsAnalysis('(()(()(')
    analysis.analyze()
    assert analysis.final_floor == 3

    analysis = FloorDirectionsAnalysis('))(((((')
    analysis.analyze()
    assert analysis.final_floor == 3

    analysis = FloorDirectionsAnalysis('())')
    analysis.analyze()
    assert analysis.final_floor == -1

    analysis = FloorDirectionsAnalysis('))(')
    analysis.analyze()
    assert analysis.final_floor == -1

    analysis = FloorDirectionsAnalysis(')())())')
    analysis.analyze()
    assert analysis.final_floor == -3


def test_analysis_malformed_sequence():
    with pytest.raises(InvalidFloorDirectionsError):
        analysis = FloorDirectionsAnalysis('(x()')
        analysis.analyze()


def test_analysis_empty_sequence():
    analysis = FloorDirectionsAnalysis('')
    analysis.analyze()
    assert analysis.final_floor == 0


def test_analysis_single_direction_sequence_opening():
    analysis = FloorDirectionsAnalysis('(')
    analysis.analyze()
    assert analysis.final_floor == 1


def test_analysis_single_direction_sequence_closing():
    analysis = FloorDirectionsAnalysis(')')
    analysis.analyze()
    assert analysis.final_floor == -1


def test_analysis_equal_number_of_opening_and_closing():
    analysis = FloorDirectionsAnalysis('()()')
    analysis.analyze()
    assert analysis.final_floor == 0


def test_analysis_only_opening_brackets():
    analysis = FloorDirectionsAnalysis('((((')
    analysis.analyze()
    assert analysis.final_floor == 4


def test_analysis_only_closing_brackets():
    analysis = FloorDirectionsAnalysis('))))')
    analysis.analyze()
    assert analysis.final_floor == -4


def test_analysis_floor_computed_without_analyze():
    analysis = FloorDirectionsAnalysis('))()((((')
    assert analysis.final_floor == 2
