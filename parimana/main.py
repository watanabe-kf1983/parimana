from pathlib import Path
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


root_dir = Path(".output")


def get_odds(*, race_id: str, recollect_odds: bool = False) -> Mapping[Eye, float]:
    base_dir = root_dir / race_id
    odds_p_path = base_dir / "odds.pickle"
    if recollect_odds or not odds_p_path.exists():
        print("scraping...")
        odds = collect_odds(race_id=race_id)
        with open(odds_p_path, "wb") as f:
            pickle.dump(odds, f)

    with open(odds_p_path, "rb") as f:
        odds = pickle.load(f)
    odds_to_csv(odds, "odds.csv")
    return odds


def main(
    *,
    race_id: str = "202305021211",
    recollect_odds: bool = False,
    num_of_simulate: int = 10_000_000,
):
    base_dir = root_dir / race_id
    print("preparing odds...")
    odds = get_odds(race_id=race_id, recollect_odds=recollect_odds)
    print("preparing distribution...")
    dist = prepare_dist(odds)
    print("analysing...")
    models = analyse(dist)

    for name, model in models.items():
        print(f"simulating {name} ...")
        model.to_csv(base_dir / name)
        chance = model.simulate(num_of_simulate)
        calc_expected_dividend_to_xl(odds, chance, base_dir / name / "result.xlsx")

    print("done.")


if __name__ == "__main__":
    main()
