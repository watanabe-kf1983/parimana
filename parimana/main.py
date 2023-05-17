from parimana.race.race import Race
from parimana.situation.situationpd import dataframes
from parimana.vote.eye import BettingType, Eye
from parimana.vote.vote import (
    VoteTallyByType,
    Odds,
)


def odds_from_text(text: str) -> Odds:
    splitted = text.split(": ")
    return Odds(Eye(splitted[0]), float(splitted[1]))


def prepare_dataframes():
    race = Race.no_absences(5, "少頭数")
    odds_data = ["1=2: 1.5", "1=3: 3.0", "1=4: 4.0", "1-2-3: 2.0", "2-1-3: 2.0"]
    odds = [odds_from_text(t) for t in odds_data]
    ratio_data = {BettingType.QUINELLA: 0.3, BettingType.TRIFECTA: 0.7}
    vote_total = 1000
    # vote_expected_data =
    # ["1=2: 160", "1=3: 80", "1=4: 60", "1-2-3: 350", "2-1-3: 350"]

    dest = race.destribution_from_odds(
        odds=odds, ratio=VoteTallyByType(ratio_data, vote_total)
    )
    return dataframes(dest)


def main():
    score, rels, members = prepare_dataframes()
    print(score)
    print(rels)


if __name__ == "__main__":
    main()
