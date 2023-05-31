from pathlib import Path

from parimana.analyse.analyse import analyse
from parimana.base.vote import calc_expected_dividend_to_xl
from parimana.driver.chrome import headless_chrome
from parimana.netkeiba.race import NetKeibaRace


root_dir = Path(".output")


def main(
    *,
    race_id: str = "202305021211",
    recollect_odds: bool = False,
    num_of_simulate: int = 10_000_000,
):
    race = NetKeibaRace(race_id, driver=headless_chrome())
    dist = race.destribution(recollect_odds)
    print("analysing...")
    models = analyse(dist)

    for name, model in models.items():
        print(f"simulating {name} ...")
        model.to_csv(race.base_dir / name)
        chance = model.simulate(num_of_simulate)
        calc_expected_dividend_to_xl(
            race.odds, chance, race.base_dir / name / "result.xlsx"
        )

    print("done.")


if __name__ == "__main__":
    main()
