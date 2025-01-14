from celery import Celery

from parimana.io.kvs import CachedStorage
from parimana.devices.redis.redis_channel import RedisChannelFactory
from parimana.devices.redis.redis_kvs import RedisStorage
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba
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

storage = CachedStorage(
    original=settings.storage.get(),
    cache=RedisStorage(settings.redis_ap_uri, "kvscache"),
)
publish_center = RedisChannelFactory(settings.redis_ap_uri).publish_center

analyse_app = AnalyseApp(store=storage)
odds_app = OddsCollectorApp(store=storage)
schedule_app = ScheduleApp(category_selector=category_selector, store=storage)
ps_manager = ProcessStatusManager(
    store=RedisStorage(settings.redis_ap_uri, "processes", ex=600),  # 10 min
    center=publish_center,
)

celery = Celery(
    "parimana",
    broker=settings.redis_q_uri,
    backend=settings.redis_q_uri,
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
    schedule_app=schedule_app,
    analyse_task_provider=analyse_tasks.scrape_and_analyse,
    task_schedule_kvs=RedisStorage(settings.redis_ap_uri, "tasks"),
    celery=celery,
)

worker = Worker(tasks_list=[analyse_tasks, schedule_tasks])
