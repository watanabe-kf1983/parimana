from typing import Mapping

import pandas as pd

from parimana.analyse.analyse import analyse
from parimana.race.race import Race
from parimana.vote.eye import BettingType, Eye


def prepare_odds() -> Mapping[Eye, float]:
    # odds_data = [
    #     "1=2: 1.5",
    #     "1=3: 3.0",
    #     "1=4: 4.0",
    #     "1-2-3: 2.0",
    #     "2-1-3: 2.0",
    #     "5-6-7: 100.0",
    #     "4-6-7: 200.0",
    #     "6: 1.1",
    #     "3: 100.0",
    #     "7: 300.0",
    #     "8: 200.0",
    # ]
    # odds = [odds_from_text(t) for t in odds_data]
    odds_data = {
        "05": 1.6,
        "02": 6.0,
        "14": 7.0,
        "12": 9.9,
        "10": 20.4,
        "11": 28.1,
        "17": 28.8,
        "18": 40.5,
        "04": 45.4,
        "01": 54.8,
        "15": 92.6,
        "08": 93.8,
        "06": 94.8,
        "07": 104.0,
        "13": 117.8,
        "16": 150.4,
        "03": 182.7,
        "09": 388.2,
    }
    return {Eye(k): v for k, v in odds_data.items()}


def prepare_dist(odds: Mapping[Eye, float]):
    race = Race.no_absences(18, "日本ダービー")

    ratio_data = {
        # https://jra.jp/company/about/financial/pdf/houkoku03.pdf p.26 別表9
        BettingType.WIN: 6.9,
        BettingType.QUINELLA: 13.3,
        BettingType.EXACTA: 5.7,
        BettingType.TRIO: 21.7,
        BettingType.TRIFECTA: 29.0,
    }
    vote_total = 100_000_000

    return race.destribution_from_odds(
        odds=odds, vote_ratio=ratio_data, vote_tally_total=vote_total
    )


def main():
    with pd.option_context(
        "display.max_rows", None, "display.max_columns", None
    ):  # more options can be specified also
        print("preparing...")
        odds = prepare_odds()
        dist = prepare_dist(odds)
        print("analysing...")
        model = analyse(dist)
        print(model.abilities)
        print(model.correlations)
        print(model.covariances)

        print("simulating...")
        chance = model.simulate(10_000_000)

        print("done.")
        # print(chance)

    # 与えられたオッズとの比を計算
    # 与えられたオッズとの比を計算


if __name__ == "__main__":
    main()
