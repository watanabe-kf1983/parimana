from parimana.analyse.analyse import analyse
from parimana.base.vote import calc_expected_dividend_to_xl
from parimana.settings import Settings


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

def main():
    settings = Settings.from_cli_args()
    race = settings.race
    dist = race.destribution(not settings.use_cache)
    print("analysing...")
    models = analyse(dist)

    chances = {}

    for name, model in models.items():
        print(f"simulating {name} ...")
        model.to_csv(race.base_dir / name)
        chance = model.simulate(settings.simulation_count)
        chances[name] = chance

    calc_expected_dividend_to_xl(
        race.odds, chances, race.base_dir / (race.race_id + ".xlsx")
    )

    print("done.")


main()
