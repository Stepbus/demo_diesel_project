from module_celery.tasks import petro_task, pilot_task, loves_task


def update_base():
    tasks = [
        petro_task,
        pilot_task,
        loves_task
    ]
    for task in tasks:
        task.apply_async()


if __name__ == "__main__":
    update_base()
