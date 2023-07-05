import pytest
from parimana.base.eye import Eye, BettingType


def test_betting_type():
    t = BettingType((True, 1, 1))
    assert t == BettingType.WIN


def test_win():
    eye = Eye("12")
    assert eye.type == BettingType.WIN
    assert eye.names == ["12"]


def test_exacta():
    eye = Eye("12-13")
    assert eye.type == BettingType.EXACTA
    assert eye.names == ["12", "13"]


def test_trifecta():
    eye = Eye("12-13-14")
    assert eye.type == BettingType.TRIFECTA
    assert eye.names == ["12", "13", "14"]


def test_quinella():
    eye = Eye("12=13")
    assert eye.type == BettingType.QUINELLA
    assert eye.names == {"12", "13"}


def test_trio():
    eye = Eye("12=13=14")
    assert eye.type == BettingType.TRIO
    assert eye.names == {"12", "13", "14"}


def test_place():
    eye = Eye("P12")
    assert eye.type == BettingType.PLACE
    assert eye.names == {"12"}


def test_show():
    eye = Eye("S12")
    assert eye.type == BettingType.SHOW
    assert eye.names == {"12"}


def test_wide():
    eye = Eye("W12=13")
    assert eye.type == BettingType.WIDE
    assert eye.names == {"12", "13"}


def test_duplicate():
    with pytest.raises(ValueError) as ve:
        eye = Eye("12=13=12")
        assert eye.type == BettingType.TRIO
    assert "duplicated" in str(ve.value)
