import pandas as pd

from parimana.analyse.analyse import analysers
from parimana.base.vote import calc_expected_dividend_df
from parimana.settings import Settings


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html


def main():
    settings = Settings.from_cli_args()
    race = settings.race
    dist = race.destribution(not settings.use_cache)

    chances = {}
    for a in analysers:
        model = a.estimate_model(dist)
        model.save_figures(race.base_dir)
        print(f"simulating {model.name} ...")
        chance = model.simulate(settings.simulation_count)
        chances[model.name] = chance

    expected = calc_expected_dividend_df(race.get_odds(), chances)
    with pd.ExcelWriter(race.base_dir / (race.race_id + ".xlsx")) as writer:
        expected.to_excel(writer, sheet_name="expected")
        expected.describe().to_excel(writer, sheet_name="description")

    print("done.")


main()
