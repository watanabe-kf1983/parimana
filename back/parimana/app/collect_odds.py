from parimana.domain.race import Race, RaceOddsPool
from parimana.io.kvs import Storage
from parimana.repository.odds import OddsRepository, OddsRepositoryImpl


class OddsCollectorApp:
    def __init__(self, store: Storage):
        self.repo: OddsRepository = OddsRepositoryImpl(store)

    def get_odds_pool(self, *, race: Race, scrape_force: bool = False) -> RaceOddsPool:
        odds_pool = self.repo.load_latest_odds_pool(race)

        if odds_pool and (odds_pool.timestamp.is_confirmed or not scrape_force):
            return odds_pool
        else:
            timestamp = race.odds_source.scrape_timestamp()
            if (not odds_pool) or odds_pool.timestamp < timestamp:
                odds_pool = race.odds_source.scrape_odds_pool()
                self.repo.save_odds_pool(odds_pool)
            return odds_pool
