import pytest
from parimana.domain.base.eye import Eye
from parimana.domain.base.contestants import Contestants


def test_contestants():
    ctt = Contestants.no_absences(180)
    assert ctt._find_contestant("002")
    assert ctt._find_contestant("180")
    with pytest.raises(ValueError) as ve:
        ctt._find_contestant("181")
    assert "Not Found" in str(ve.value)


def test_situation():
    situation = Contestants.no_absences(5).situation(Eye("2=3=4"))

    assert [str(r) for r in situation.relations] == [
        "1=1",
        "1<2",
        "1<3",
        "1<4",
        "1?5",
        "2>1",
        "2=2",
        "2?3",
        "2?4",
        "2>5",
        "3>1",
        "3?2",
        "3=3",
        "3?4",
        "3>5",
        "4>1",
        "4?2",
        "4?3",
        "4=4",
        "4>5",
        "5?1",
        "5<2",
        "5<3",
        "5<4",
        "5=5",
    ]
