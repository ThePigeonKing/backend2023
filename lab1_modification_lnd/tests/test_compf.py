import sys
from pathlib import Path
import pytest

# add dir to syspath
sys.path.append(str(Path(__file__).parent.parent))

from compf import Compf


@pytest.fixture
def compf():
    return Compf()


def test_single_number(compf):
    assert compf.compile("III") == "0b11"


def test_simple_addition(compf):
    assert compf.compile("I+II") == "0b1 0b10 +"


def test_simple_subtraction(compf):
    assert compf.compile("V-I") == "0b101 0b1 -"


def test_combined_operations(compf):
    assert compf.compile("V-I+II") == "0b101 0b1 - 0b10 +"


def test_operation_with_parentheses(compf):
    assert compf.compile("(V-I)+II") == "0b101 0b1 - 0b10 +"


def test_complex_expression(compf):
    assert compf.compile("((V-I)+II)*III/IV") == "0b101 0b1 - 0b10 + 0b11 * 0b100 /"
