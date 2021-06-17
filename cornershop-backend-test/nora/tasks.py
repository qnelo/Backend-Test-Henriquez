from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from .order_generator import create_orders

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute="0", hour="8,10")), name="place_orders_for_the_day"
)
def place_orders_for_the_day():
    logger.info("place_orders_for_the_day")

    return create_orders()
