import pandas as pd
from parimana.analyse.analyse import analyse
from parimana.race.race import Race
from parimana.vote.eye import BettingType, Eye
from parimana.vote.vote import (
    VoteTallyByType,
    Odds,
)


def odds_from_text(text: str) -> Odds:
    splitted = text.split(": ")
    return Odds(Eye(splitted[0]), float(splitted[1]))


def prepare_dist():
    race = Race.no_absences(18, "日本ダービー")

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
        "05": 2.9,
        "02": 4.6,
        "14": 7.7,
        "12": 8.1,
        "18": 15.7,
        "11": 19.7,
        "06": 23.3,
        "08": 24.6,
        "10": 29.5,
        "04": 30.9,
        "17": 31.1,
        "07": 32.4,
        "01": 41.2,
        "15": 43.9,
        "13": 44.4,
        "16": 59.1,
        "03": 68,
        "09": 133.4,
    }
    odds = [Odds(Eye(k), v) for k, v in odds_data.items()]
    ratio_data = {
        BettingType.QUINELLA: 0.0,
        BettingType.TRIFECTA: 0.0,
        BettingType.WIN: 1.0,
    }
    vote_total = 1_000_000

    return race.destribution_from_odds(
        odds=odds, ratio=VoteTallyByType(ratio_data, vote_total)
    )


def main():
    with pd.option_context(
        "display.max_rows", None, "display.max_columns", None
    ):  # more options can be specified also
        dist = prepare_dist()
        model = analyse(dist)

        result = model.simulate(10_000_000)

        print(result)

    # 与えられたオッズとの比を計算
    # 与えられたオッズとの比を計算


if __name__ == "__main__":
    main()
