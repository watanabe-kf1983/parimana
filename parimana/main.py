from parimana.analyse.analyse import analyse
from parimana.race.race import Race
from parimana.vote.eye import BettingType, Eye
from parimana.vote.vote import (
    VoteTallyByType,
    Odds,
)


def odds_from_text(text: str) -> Odds:
    splitted = text.split(": ")
    return Odds(Eye(splitted[0]), float(splitted[1]))


def prepare_dist():
    race = Race.no_absences(8, "少頭数")
    odds_data = [
        "1=2: 1.5",
        "1=3: 3.0",
        "1=4: 4.0",
        "1-2-3: 2.0",
        "2-1-3: 2.0",
        "5-6-7: 100.0",
        "4-6-7: 200.0",
        "1: 1.1",
        "3: 100.0",
        "7: 300.0",
        "8: 200.0",
    ]
    odds = [odds_from_text(t) for t in odds_data]
    ratio_data = {
        BettingType.QUINELLA: 0.3,
        BettingType.TRIFECTA: 0.6,
        BettingType.WIN: 0.1,
    }
    vote_total = 1000

    return race.destribution_from_odds(
        odds=odds, ratio=VoteTallyByType(ratio_data, vote_total)
    )


def main():
    dist = prepare_dist()
    model = analyse(dist)
    print(model)


if __name__ == "__main__":
    main()
