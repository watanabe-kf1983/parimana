from functools import cached_property
from typing import Sequence, Type

from celery import Celery

from parimana.io.kvs import CachedStorage, Storage
from parimana.io.message import PublishCenter
from parimana.domain.race import Race, RaceSelector
from parimana.domain.schedule import Category, CategorySelector
from parimana.app import AnalyseApp, OddsCollectorApp, ProcessStatusManager, ScheduleApp
from parimana.tasks import AnalyseTasks, ScheduleTasks, Worker
from parimana.devices.redis.redis_channel import RedisChannelFactory
from parimana.devices.redis.redis_kvs import RedisStorage
from parimana.devices.s3.s3_kvs import S3Storage
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba
from parimana.settings import Settings


class _ParimanaContext:

    @cached_property
    def race_types(self) -> Sequence[Type[Race]]:
        return [BoatRace, NetKeibaRace]

    @cached_property
    def categories(self) -> Sequence[Category]:
        return [category_boat, category_keiba]

    @cached_property
    def race_selector(self) -> RaceSelector:
        return RaceSelector(self.race_types)

    @cached_property
    def category_selector(self) -> CategorySelector:
        return CategorySelector(self.categories)

    @cached_property
    def settings(self) -> Settings:
        return Settings()

    @cached_property
    def storage(self) -> Storage:
        _storage = self.settings.storage.get()

        if isinstance(_storage, S3Storage):
            _storage = CachedStorage(
                original=_storage,
                cache=RedisStorage(self.settings.redis_ap_uri, "kvscache"),
            )

        return _storage

    @cached_property
    def publish_center(self) -> PublishCenter:
        return RedisChannelFactory(self.settings.redis_ap_uri).publish_center

    @cached_property
    def analyse_app(self) -> AnalyseApp:
        return AnalyseApp(store=self.storage)

    @cached_property
    def odds_app(self) -> OddsCollectorApp:
        return OddsCollectorApp(store=self.storage)

    @cached_property
    def schedule_app(self) -> ScheduleApp:
        return ScheduleApp(category_selector=self.category_selector, store=self.storage)

    @cached_property
    def ps_manager(self) -> ProcessStatusManager:
        return ProcessStatusManager(
            store=RedisStorage(
                self.settings.redis_ap_uri, "processes", ex=600
            ),  # 10 min
            center=self.publish_center,
        )

    @cached_property
    def celery(self) -> Celery:
        return Celery(
            "parimana",
            broker=self.settings.redis_q_uri,
            backend=self.settings.redis_q_uri,
            config_source="parimana.tasks.celeryconfig",
        )

    @cached_property
    def analyse_tasks(self) -> AnalyseTasks:
        return AnalyseTasks(
            analyse_app=self.analyse_app,
            odds_app=self.odds_app,
            ps_manager=self.ps_manager,
            race_selector=self.race_selector,
            celery=self.celery,
            publish_center=self.publish_center,
        )

    @cached_property
    def schedule_tasks(self) -> ScheduleTasks:
        return ScheduleTasks(
            schedule_app=self.schedule_app,
            analyse_task_provider=self.analyse_tasks.scrape_and_analyse,
            task_schedule_kvs=RedisStorage(self.settings.redis_ap_uri, "tasks"),
            celery=self.celery,
        )

    @cached_property
    def worker(self) -> Worker:
        return Worker(tasks_list=[self.analyse_tasks, self.schedule_tasks])


context: _ParimanaContext = _ParimanaContext()
