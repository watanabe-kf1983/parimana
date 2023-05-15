from parimana.race.race import Race
from parimana.vote.eye import BettingType, Eye
from parimana.vote.vote import (
    VoteTallyByType,
    Odds,
)
from parimana.race.race import (
    Race,
)


def odds_from_text(text: str) -> Odds:
    splitted = text.split(": ")
    return Odds(Eye(splitted[0]), float(splitted[1]))


def test_race_vote():
    race = Race.no_absences(5, "少頭数")
    odds_data = ["1=2: 1.5", "1=3: 3.0", "1=4: 4.0", "1-2-3: 2.0", "2-1-3: 2.0"]
    odds = [odds_from_text(t) for t in odds_data]
    ratio_data = {BettingType.QUINELLA: 0.3, BettingType.TRIFECTA: 0.7}
    vote_total = 1000
    # vote_expected_data =
    # ["1=2: 160", "1=3: 80", "1=4: 60", "1-2-3: 350", "2-1-3: 350"]

    destribution = race.destribution_from_odds(
        odds=odds, ratio=VoteTallyByType(ratio_data, vote_total)
    )
    print(destribution)

    assert False
