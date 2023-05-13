import pytest
from parimana.base.eye import Eye, BettingType


def test_betting_type():
    t = BettingType((True, 1))
    assert t == BettingType.WIN


def test_win():
    eye = Eye("12")
    assert eye.type == BettingType.WIN


def test_exacta():
    eye = Eye("12-13")
    assert eye.type == BettingType.EXACTA


def test_trifecta():
    eye = Eye("12-13-14")
    assert eye.type == BettingType.TRIFECTA


def test_quinella():
    eye = Eye("12=13")
    assert eye.type == BettingType.QUINELLA


def test_trio():
    eye = Eye("12=13=14")
    assert eye.type == BettingType.TRIO


def test_duplicate():
    with pytest.raises(ValueError) as ve:
        eye = Eye("12=13=12")
        assert eye.type == BettingType.TRIO
    assert "duplicated" in str(ve.value)
