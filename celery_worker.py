from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "device_monitoring",
    broker=settings.CELERY_BROKER_URL,
    include=["app.tasks.analytics"]
)

celery_app.conf.update(
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    celery_app.start()