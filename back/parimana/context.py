from celery import Celery

from parimana.devices.redis.redis_channel import RedisChannelFactory
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba
from parimana.io.kvs import FileStorage
from parimana.domain.race import RaceSelector
from parimana.domain.schedule import CategorySelector
from parimana.app import AnalyseApp, OddsCollectorApp, ProcessStatusManager, ScheduleApp
from parimana.tasks import AnalyseTasks, ScheduleTasks, Worker
from parimana.settings import Settings

race_types = [BoatRace, NetKeibaRace]
categories = [category_boat, category_keiba]
race_selector = RaceSelector(race_types)
category_selector = CategorySelector(categories)


settings = Settings()

storage = FileStorage(settings.file_storage_root_path)
publish_center = RedisChannelFactory(settings.redis_uri).publish_center


analyse_app = AnalyseApp(store=storage)
odds_app = OddsCollectorApp(store=storage)
schedule_app = ScheduleApp(category_selector=category_selector, store=storage)
ps_manager = ProcessStatusManager(store=storage, center=publish_center)

celery = Celery(
    "parimana",
    broker=settings.redis_uri,
    backend=settings.redis_uri,
    config_source="parimana.tasks.celeryconfig",
)

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

worker = Worker(tasks_list=[analyse_tasks, schedule_tasks])
