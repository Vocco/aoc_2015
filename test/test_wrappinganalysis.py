import time

from os import path as ospath
from sys import path as syspath
from unittest.mock import Mock

import pytest

syspath.append(ospath.abspath('../'))

from presentdimensions import PresentDimensions
from wrappinganalysis import WrappingAnalysis


# unit tests
def test_total_wrapping_paper_required_happy_path():
    mock_present_1 = Mock(spec=PresentDimensions)
    mock_present_1.surface_area = 58
    mock_present_1.smallest_side_area = 6
    mock_present_2 = Mock(spec=PresentDimensions)
    mock_present_2.surface_area = 43
    mock_present_2.smallest_side_area = 1

    analysis = WrappingAnalysis([mock_present_1, mock_present_2])
    assert analysis.total_wrapping_paper_required == 108


def test_total_wrapping_paper_required_single_present():
    mock_present = Mock(spec=PresentDimensions)
    mock_present.surface_area = 58
    mock_present.smallest_side_area = 6

    analysis = WrappingAnalysis([mock_present])
    assert analysis.total_wrapping_paper_required == 64


def test_total_wrapping_paper_required_empty():
    analysis = WrappingAnalysis([])
    assert analysis.total_wrapping_paper_required == 0


def test_wrapping_paper_required_2_3_4():
    mock_present = Mock(spec=PresentDimensions)
    mock_present.surface_area = 52
    mock_present.smallest_side_area = 6

    result = WrappingAnalysis.wrapping_paper_required(mock_present)
    assert result == 58

def test_wrapping_paper_required_1_1_10():
    mock_present = Mock(spec=PresentDimensions)
    mock_present.surface_area = 42
    mock_present.smallest_side_area = 1

    result = WrappingAnalysis.wrapping_paper_required(mock_present)
    assert result == 43


def test_not_a_list_arg():
    with pytest.raises(TypeError):
        WrappingAnalysis(Mock(spec=PresentDimensions))


def test_not_present_dimensions():
    not_present_dimensions = dict(surface_area=42, smallest_side_area=1)

    with pytest.raises(TypeError):
        WrappingAnalysis.wrapping_paper_required(not_present_dimensions)


# performance tests
@pytest.mark.perf
def test_wrapping_analysis_total_wrapping_paper_required_large_input():
    mock_dimensions = Mock(spec=PresentDimensions)
    mock_dimensions.surface_area = 6
    mock_dimensions.smallest_side_area = 1
    analysis = WrappingAnalysis([mock_dimensions] * 1_000_000)

    start = time.perf_counter()
    result = analysis.total_wrapping_paper_required
    end = time.perf_counter()

    assert end - start < 1.0
    assert result == 7_000_000
