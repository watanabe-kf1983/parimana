import pickle
from typing import Mapping

from parimana.analyse.analyse import analyse
from parimana.base.race import Race
from parimana.base.eye import BettingType, Eye
from parimana.base.vote import calc_expected_dividend_to_xl, odds_to_csv
from parimana.scrape.main import collect_odds


def prepare_dist(odds: Mapping[Eye, float]):
    race = Race.no_absences(18, "日本ダービー")

    # ratio_data = {
    #     # https://jra.jp/company/about/financial/pdf/houkoku03.pdf p.26 別表9
    #     BettingType.WIN: 6.9,
    #     BettingType.QUINELLA: 13.3,
    #     BettingType.EXACTA: 5.7,
    #     BettingType.TRIO: 21.7,
    #     BettingType.TRIFECTA: 29.0,
    # }
    ratio_data_derby = {
        # https://jra-van.jp/fun/baken/index3.html
        BettingType.WIN: 6.3,
        BettingType.QUINELLA: 16.3,
        BettingType.EXACTA: 6.3,
        BettingType.TRIO: 19.5,
        BettingType.TRIFECTA: 37.1,
    }

    vote_total = 100_000_000

    return race.destribution_from_odds(
        odds=odds, vote_ratio=ratio_data_derby, vote_tally_total=vote_total
    )


def main():
    # print("scraping...")
    # odds = collect_odds()
    # with open("odds.pickle", "wb") as f:
    #     pickle.dump(odds, f)
    with open("odds.pickle", "rb") as f:
        odds = pickle.load(f)
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
