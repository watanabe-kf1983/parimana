from parimana.base.superiority import iterate_relation


def test_superiority_trifecta():
    relations = [str(r) for r in sorted(iterate_relation([6, 5, 4], {3, 2}))]
    assert relations == [
        "2=2",
        "2?3",
        "2<4",
        "2<5",
        "2<6",
        "3=3",
        "3<4",
        "3<5",
        "3<6",
        "4=4",
        "4<5",
        "4<6",
        "5=5",
        "5<6",
        "6=6",
    ]


def test_superiority_trio():
    relations = [str(r) for r in sorted(iterate_relation({6, 5, 4}, {3, 2}))]
    assert relations == [
        "2=2",
        "2?3",
        "2<4",
        "2<5",
        "2<6",
        "3=3",
        "3<4",
        "3<5",
        "3<6",
        "4=4",
        "4?5",
        "4?6",
        "5=5",
        "5?6",
        "6=6",
    ]
