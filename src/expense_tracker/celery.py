import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')

app = Celery('expense_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Add the beat schedule here
app.conf.beat_schedule = {
    'send-reminder-emails': {
        'task': 'expenses.tasks.send_reminder_emails',
        'schedule': crontab(hour=17, minute=15),  # Daily at 8 AM
    },
    'check-budget-thresholds': {
        'task': 'expenses.tasks.check_budget_thresholds',
        'schedule': crontab(hour=17, minute=15, day_of_month='13'),  # First day of month at 9 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')