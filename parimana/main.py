from pathlib import Path

from parimana.analyse.analyse import analyse
from parimana.base.race import Race
from parimana.base.vote import calc_expected_dividend_to_xl
from parimana.boatrace.race import BoatRace
from parimana.driver.chrome import headless_chrome
from parimana.netkeiba.race import NetKeibaRace


root_dir = Path(".output")


def get_race() -> Race:
    return BoatRace(date="20230531", cource=1, number=10)
    # return NetKeibaRace(race_id="202305021211", driver=headless_chrome())


def main(
    *,
    recollect_odds: bool = True,
    num_of_simulate: int = 10_000_000,
):
    race = get_race()
    dist = race.destribution(recollect_odds)
    print("analysing...")
    models = analyse(dist)

    chances = {}

    for name, model in models.items():
        print(f"simulating {name} ...")
        model.to_csv(race.base_dir / name)
        chance = model.simulate(num_of_simulate)
        chances[name] = chance

    calc_expected_dividend_to_xl(
        race.odds, chances, race.base_dir / (race.race_id + ".xlsx")
    )

    print("done.")


if __name__ == "__main__":
    main()
