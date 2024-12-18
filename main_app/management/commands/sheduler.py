from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from main_app.utils.cron_task import start_amazon_auto_task, start_aliexpress_auto_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Scheduler started")
        scheduler = BlockingScheduler()

        scheduler.add_job(start_amazon_auto_task,
                          CronTrigger.from_crontab("0 */4 * * *", timezone='UTC'))
        scheduler.add_job(start_aliexpress_auto_task,
                          CronTrigger.from_crontab("0 */4 * * *", timezone='UTC'))
        scheduler.start()
        print("Scheduler exited")
        # "0 */1 * * *"
