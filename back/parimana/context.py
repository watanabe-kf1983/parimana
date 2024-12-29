from celery import Celery

from parimana.devices.redis.redis_channel import RedisChannelFactory
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba
from parimana.io.kvs import FileStorage
from parimana.domain.race import RaceSelector
from parimana.app import AnalyseApp, OddsCollectorApp, ProcessStatusManager, ScheduleApp
from parimana.tasks import AnalyseTasks, ScheduleTasks, Worker
import parimana.settings as settings

race_types = [BoatRace, NetKeibaRace]
categories = [category_boat, category_keiba]


storage = FileStorage(settings.FILE_STORAGE_ROOT_PATH)
publish_center = RedisChannelFactory(settings.REDIS_DB_URI).publish_center


analyse_app = AnalyseApp(store=storage)
odds_app = OddsCollectorApp(store=storage)
schedule_app = ScheduleApp(categories=categories, store=storage)
ps_manager = ProcessStatusManager(store=storage, center=publish_center)
race_selector = RaceSelector(race_types)

celery = Celery("parimana", config_source="parimana.celeryconfig")
worker = Worker(celery=celery)

analyse_tasks = AnalyseTasks(
    analyse_app=analyse_app,
    odds_app=odds_app,
    ps_manager=ps_manager,
    race_selector=race_selector,
    celery=celery,
    publish_center=publish_center,
)

schedule_tasks = ScheduleTasks(
    schedule_app=schedule_app, celery=celery, publish_center=publish_center
)
