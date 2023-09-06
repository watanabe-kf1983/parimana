from parimana.base.superiority import Superiority
from parimana.base.situation import Situation


def test_situation_score():
    rs = Situation.from_collections(([2, 3, 4], {1, 5}))

    assert [f"{k}: {v}" for k, v in rs.scores.items()] == [
        "1: -3",
        "2: 4",
        "3: 2",
        "4: 0",
        "5: -3",
    ]


def test_situation_superiority():
    rs = Situation.from_collections(([2, 3, 4], {1, 5}))

    assert rs.get_superiority(1, 1) == Superiority.EQUALS
    assert rs.get_superiority(1, 2) == Superiority.INFERIOR
    assert rs.get_superiority(1, 5) == Superiority.UNKNOWN
    assert rs.get_superiority(2, 1) == Superiority.SUPERIOR
