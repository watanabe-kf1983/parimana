from parimana.base.eye import BettingType, Eye
from parimana.base.vote import (
    calc_vote_tally,
)


def test_calc_vote_tally():
    odds_data = {"1=2": 1.5, "1=3": 3.0, "1=4": 4.0, "1-2-3": 2.0, "2-1-3": 2.0}
    ratio_data = {BettingType.QUINELLA: 0.3, BettingType.TRIFECTA: 0.7}
    vote_total = 1000
    vote_expected_data = {"1=2": 160, "1=3": 80, "1=4": 60, "1-2-3": 350, "2-1-3": 350}
    odds = {Eye(k): v for k, v in odds_data.items()}
    expected = {Eye(k): v for k, v in vote_expected_data.items()}

    assert calc_vote_tally(odds, ratio_data, vote_total) == expected
