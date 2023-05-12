from parimana.base.rank import MixedRankCounter


def test_selection():
    mrc = MixedRankCounter([1, 2, 3], {4, 5, 6})
    assert mrc.rank_zero_ave(1) == 2.5
    assert mrc.rank_zero_ave(2) == 1.5
    assert mrc.rank_zero_ave(3) == 0.5
    assert mrc.rank_zero_ave(4) == -1.5
    assert mrc.rank_zero_ave(5) == -1.5
    assert mrc.rank_zero_ave(6) == -1.5


def test_rank_trio():
    mrc = MixedRankCounter({1, 2, 3}, {4, 5, 6})
    assert mrc.rank_zero_ave(1) == 1.5
    assert mrc.rank_zero_ave(2) == 1.5
    assert mrc.rank_zero_ave(3) == 1.5
    assert mrc.rank_zero_ave(4) == -1.5
    assert mrc.rank_zero_ave(5) == -1.5
    assert mrc.rank_zero_ave(6) == -1.5
