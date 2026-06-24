from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.services.collectors.registry import collector_registry


class SchedulerService:
    def __init__(self) -> None:
        self.interval_minutes = settings.collection_interval_minutes
        self._scheduler = BackgroundScheduler(timezone="UTC")

    @property
    def is_running(self) -> bool:
        return self._scheduler.running

    def start(self) -> None:
        if self._scheduler.running:
            return
        self._scheduler.add_job(
            self.run_collection_once,
            "interval",
            minutes=self.interval_minutes,
            id="collect_real_estate_listings",
            replace_existing=True,
            max_instances=1,
        )
        self._scheduler.start()

    def stop(self) -> None:
        if self._scheduler.running:
            self._scheduler.shutdown(wait=False)

    def run_collection_once(self) -> dict[str, object]:
        return collector_registry.collect_all()


scheduler_service = SchedulerService()

