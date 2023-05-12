import pytest
from parimana.base.race import Race


def test_race():
    race = Race.no_absences(18, "Full Gate")
    assert race.find_contestant("2")
    assert race.find_contestant("18")
    with pytest.raises(ValueError) as ve:
        race.find_contestant("19")
    assert "Not Found" in str(ve.value)
