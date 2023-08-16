from parimana.analyse.analyse import AnalysisResult
from parimana.settings import Settings


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html


def main():
    settings = Settings.from_cli_args()
    race = settings.race
    if not settings.use_cache:
        race.remove_odds_cache()

    for a in settings.analysers:
        r = a.analyse(race=race, simulation_count=settings.simulation_count)
        r.save(race.base_dir / a.name)
        print_recommendation(r, settings.recommend_query, settings.recommend_size)


def print_recommendation(r: AnalysisResult, query: str, size: int):
    rec = r.recommendation
    if query:
        rec = rec.query(query)
    rec = rec.head(size)
    print()
    print(f"-- Recommendation by {r.model.name} [{query}] --")
    print(rec)
    print()


main()
