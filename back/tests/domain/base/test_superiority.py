from parimana.domain.base.superiority import iterate_relation


def test_iteration_trifecta():
    iterated = [str(r) for r in sorted(iterate_relation([6, 5, 4], {3, 2}))]
    assert iterated == [
        "2=2",
        "2?3",
        "2<4",
        "2<5",
        "2<6",
        "3?2",
        "3=3",
        "3<4",
        "3<5",
        "3<6",
        "4>2",
        "4>3",
        "4=4",
        "4<5",
        "4<6",
        "5>2",
        "5>3",
        "5>4",
        "5=5",
        "5<6",
        "6>2",
        "6>3",
        "6>4",
        "6>5",
        "6=6",
    ]


def test_iteration_trio():
    iterated = [str(r) for r in sorted(iterate_relation({6, 5, 4}, {3, 2}))]
    assert iterated == [
        "2=2",
        "2?3",
        "2<4",
        "2<5",
        "2<6",
        "3?2",
        "3=3",
        "3<4",
        "3<5",
        "3<6",
        "4>2",
        "4>3",
        "4=4",
        "4?5",
        "4?6",
        "5>2",
        "5>3",
        "5?4",
        "5=5",
        "5?6",
        "6>2",
        "6>3",
        "6?4",
        "6?5",
        "6=6",
    ]
