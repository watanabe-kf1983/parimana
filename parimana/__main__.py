from parimana.settings import Settings


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html


def main():
    settings = Settings.from_cli_args()
    race = settings.race
    if not settings.use_cache:
        race.remove_odds_cache()
    odds = race.odds
    dist = race.extract_destribution()

    for a in settings.analysers:
        r = a.analyse(odds=odds, dist=dist, simulation_count=settings.simulation_count)
        r.save(race.base_dir / a.name)
        r.print_recommend()

    print("done.")


main()
