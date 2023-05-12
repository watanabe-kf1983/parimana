import pytest
from parimana.base.eye import Eye


def test_win():
    eye = Eye("12")
    assert eye.type == "WIN"
    assert eye.is_sequencial


def test_exacta():
    eye = Eye("12-13")
    assert eye.type == "EXACTA"
    assert eye.is_sequencial


def test_trifecta():
    eye = Eye("12-13-14")
    assert eye.type == "TRIFECTA"
    assert eye.is_sequencial


def test_quinella():
    eye = Eye("12=13")
    assert eye.type == "QUINELLA"
    assert not eye.is_sequencial


def test_trio():
    eye = Eye("12=13=14")
    assert eye.type == "TRIO"
    assert not eye.is_sequencial


def test_duplicate():
    with pytest.raises(ValueError) as ve:
        eye = Eye("12=13=12")
        assert eye.type == "TRIO"
    assert "duplicated" in str(ve.value)
