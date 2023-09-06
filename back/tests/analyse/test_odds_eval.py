from parimana.base.eye import BettingType, Eye
from parimana.base.odds import NormalOdds
from parimana.analyse.odds_eval import (
    calc_vote_tally,
)
import math


def test_calc_vote_tally():
    odds_data = {"1=2": 1.5, "1=3": 3.0, "1=4": 4.0, "1-2-3": 2.0, "2-1-3": 2.0}
    ratio_data = {BettingType.QUINELLA: 0.3, BettingType.TRIFECTA: 0.7}
    vote_expected_data = {
        "1=2": 0.160,
        "1=3": 0.080,
        "1=4": 0.060,
        "1-2-3": 0.350,
        "2-1-3": 0.350,
    }
    odds = {Eye(k): NormalOdds(v) for k, v in odds_data.items()}
    expected = {Eye(k): v for k, v in vote_expected_data.items()}
    actual = calc_vote_tally(odds, ratio_data)

    for k, v in expected.items():
        math.isclose(actual[k], expected[k])
