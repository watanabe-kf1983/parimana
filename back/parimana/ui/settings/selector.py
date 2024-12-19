from parimana.domain.race import RaceSelector
from parimana.domain.schedule import CategorySelector
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba

race_selector = RaceSelector([BoatRace, NetKeibaRace])
category_selector = CategorySelector([category_boat, category_keiba])
