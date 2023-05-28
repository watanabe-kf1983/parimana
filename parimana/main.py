from typing import Mapping

from parimana.analyse.analyse import analyse
from parimana.base.race import Race
from parimana.base.eye import BettingType, Eye
from parimana.base.vote import calc_expected_dividend_to_xl, odds_to_csv
from parimana.scrape.main import collect_odds


def prepare_odds() -> Mapping[Eye, float]:
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
    print("scraping...")
    odds = collect_odds()
    # odds = prepare_odds()
    odds_to_csv(odds, "odds.csv")

    print("preparing...")
    dist = prepare_dist(odds)
    print("analysing...")
    model = analyse(dist)
    model.to_csv("model")

    print("simulating...")
    chance = model.simulate(10_000_000)
    calc_expected_dividend_to_xl(odds, chance, "result.xlsx")

    print("done.")


if __name__ == "__main__":
    main()
