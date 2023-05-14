from parimana.base.race import Contestant, Race
from parimana.base.eye import Eye
from parimana.base.selection import Selection
from parimana.base.superiority import Superiority


def test_selection():
    race = Race.no_absences(5, "少頭数")
    selection = Selection(race, Eye("2=3=4"))

    assert [str(r) for r in selection.relations.relations] == [
        "1=1",
        "1<2",
        "1<3",
        "1<4",
        "1?5",
        "2=2",
        "2?3",
        "2?4",
        "2>5",
        "3=3",
        "3?4",
        "3>5",
        "4=4",
        "4>5",
        "5=5",
    ]


def test_relations_score():
    race = Race.no_absences(5, "少頭数")
    relations = Selection(race, Eye("2-3-4")).relations
    assert [f"{k}: {v}" for k, v in relations._score_mapping.items()] == [
        "1: -3",
        "2: 4",
        "3: 2",
        "4: 0",
        "5: -3",
    ]


def test_relations_mapping():
    race = Race.no_absences(5, "少頭数")
    relations = Selection(race, Eye("2-3-4")).relations
    assert (
        relations.get_superiority(Contestant("1"), Contestant("1"))
        == Superiority.EQUALS
    )
    assert (
        relations.get_superiority(Contestant("1"), Contestant("2"))
        == Superiority.INFERIOR
    )
    assert (
        relations.get_superiority(Contestant("1"), Contestant("5"))
        == Superiority.UNKNOWN
    )
    assert (
        relations.get_superiority(Contestant("2"), Contestant("1"))
        == Superiority.SUPERIOR
    )
