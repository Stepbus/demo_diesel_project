import logging
from time import sleep

from celery.schedules import crontab

from scrapers.loves_scraper import handler_loves
from module_celery.celery_app import app
from scrapers.pilot_scraper import handler_pilot
from scrapers.ta_petro_scraper import handler_ta_petro


@app.task()
def petro_task():
    for attempt in range(3):
        try:
            handler_ta_petro(0)
        except Exception as error:
            logging.warning(error)
            sleep(5)
            continue
        else:
            break


@app.task()
def pilot_task():
    for attempt in range(4):
        try:
            handler_pilot()
        except Exception as error:
            logging.warning(error)
            sleep(10)
            continue
        else:
            break


@app.task
def loves_task():
    for attempt in range(3):
        try:
            handler_loves()
        except Exception as error:
            logging.warning(error)
            sleep(5)
            continue
        else:
            break


@app.task(name="update_base")
def update_base():
    tasks = [petro_task,
             pilot_task,
             loves_task
             ]
    for task in tasks:
        task.apply_async()


app.conf.beat_schedule = {
    'DB_updating': {
        'task': 'update_base',
        'schedule': crontab(minute=10, hour=6),
    },
}
app.conf.timezone = 'UTC'
