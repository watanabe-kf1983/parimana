import pytest
from parimana.vote.eye import Eye
from parimana.race.race import Race


def test_race():
    race = Race.no_absences(180, "Full Gate")
    assert race._find_contestant("002")
    assert race._find_contestant("180")
    with pytest.raises(ValueError) as ve:
        race._find_contestant("181")
    assert "Not Found" in str(ve.value)


def test_situation():
    situation = Race.no_absences(5, "少頭数").situation(Eye("2=3=4"))

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
