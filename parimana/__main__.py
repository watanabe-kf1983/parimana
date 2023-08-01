from parimana.settings import Settings


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html


def main():
    settings = Settings.from_cli_args()
    race = settings.race
    if not settings.use_cache:
        race.remove_odds_cache()

    for a in settings.analysers:
        r = a.analyse(
            race=race, simulation_count=settings.simulation_count
        )
        r.print_recommend()
        r.save(race.base_dir / a.name)


main()
