from parimana.analyse.analyse import AnalysisResult
from parimana.settings import Settings
import parimana.batch as batch


# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html


def main():
    settings = Settings.from_cli_args()
    results = batch.main(settings)
    for result in results:
        print_recommendation(result, settings.recommend_query, settings.recommend_size)


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
