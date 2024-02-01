import sys
from pathlib import Path
import pytest

# add dir to syspath
sys.path.append(str(Path(__file__).parent.parent))
from calcnew import CalcNew


@pytest.fixture
def calc_new():
    return CalcNew()


@pytest.mark.parametrize(
    "expression,expected_result",
    [
        ("I+I", 2),
        ("II*III", 6),
        ("IV-II", 2),
        ("VIII/II", 4),
        ("I+II*III-IV/II", 5),
    ],
)
def test_evaluate(calc_new, expression, expected_result):
    result = calc_new.evaluate(expression)
    assert result == expected_result, f"Ожидалось {expected_result}, получено {result}"
