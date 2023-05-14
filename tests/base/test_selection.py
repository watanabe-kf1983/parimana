from parimana.base.race import Race
from parimana.base.selection import Selection


def test_selection():
    race = Race.no_absences(5, "少頭数")
    selection = Selection.from_text(race, "2=3=4")

    assert {str(r) for r in selection.relations} == {
        "2>1",
        "3>1",
        "4>1",
        "2>5",
        "3>5",
        "4>5",
    }
