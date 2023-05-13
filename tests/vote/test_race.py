from parimana.base.race import Race
from parimana.base.eye import BettingType
from parimana.vote.odds import (
    VoteTally,
    VoteTallyByType,
    Odds,
)
from parimana.vote.race import (
    RaceOdds,
)


race = Race.no_absences(5, "少頭数")
odds_data = ["1=2: 1.5", "1=3: 3.0", "1=4: 4.0", "1-2-3: 2.0", "2-1-3: 2.0"]
odds = [Odds.from_text(t) for t in odds_data]
ratio_data = {BettingType.QUINELLA: 0.3, BettingType.TRIFECTA: 0.7}
vote_total = 1000

race_odds = RaceOdds(race, odds)
race_vote = race_odds.estimate_vote(VoteTallyByType(ratio_data, vote_total))


def test_race_odds():
    vote_expected_data = ["1=2: 160", "1=3: 80", "1=4: 60", "1-2-3: 350", "2-1-3: 350"]
    expected = [VoteTally.from_text(t) for t in vote_expected_data]

    assert race_vote.vote_tallies == expected


def test_race_vote():
    print(race_vote.relations)
    print(race_vote.ranks)

    assert False
