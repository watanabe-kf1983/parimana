from parimana.base.superiority import RelationIterator


def test_superiority_trifecta():
    ri = RelationIterator([6, 5, 4], {3, 2})
    relations = {str(r) for r in ri.iterator()}
    assert relations == {"6>5", "6>4", "6>3", "6>2", "5>4", "5>3", "5>2", "4>3", "4>2"}


def test_superiority_trio():
    ri = RelationIterator({6, 5, 4}, {3, 2})
    relations = {str(r) for r in ri.iterator()}
    assert relations == {"6>3", "6>2", "5>3", "5>2", "4>3", "4>2"}
