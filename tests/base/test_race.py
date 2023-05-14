import pytest
from parimana.base.race import Race


def test_race():
    race = Race.no_absences(180, "Full Gate")
    assert race.find_contestant("002")
    assert race.find_contestant("180")
    with pytest.raises(ValueError) as ve:
        race.find_contestant("181")
    assert "Not Found" in str(ve.value)
