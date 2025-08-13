import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.db import models
from .models import Budget, Expense, Reminder

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_emails():
    """Send scheduled reminder emails with robust error handling"""
    today = timezone.now().date()
    reminders = Reminder.objects.filter(
        due_date__lte=today,
        email_sent=False
    ).select_related('user')
    
    logger.info(f"Found {len(reminders)} reminders to process")
    
    for reminder in reminders:
        try:
            subject = f"Reminder: {reminder.title}"
            context = {'reminder': reminder, 'site_name': 'Expense Tracker'}
            message = render_to_string('emails/reminder.html', context)
            text_message = render_to_string('emails/reminder.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reminder.user.email],
                fail_silently=False,
            )
            reminder.email_sent = True
            reminder.save()
            logger.info(f"Sent reminder email for reminder ID: {reminder.id}")
        except Exception as e:
            logger.error(f"Failed to send reminder {reminder.id}: {str(e)}", exc_info=True)

@shared_task
def check_budget_thresholds():
    """Check budget thresholds and send alerts with improved performance"""
    today = timezone.now().date()
    active_budgets = Budget.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).select_related('user', 'category')
    
    logger.info(f"Processing {len(active_budgets)} active budgets")
    
    for budget in active_budgets:
        try:
            # Aggregate spending in a single query
            filters = {
                'user': budget.user,
                'date__range': [budget.start_date, budget.end_date]
            }
            if budget.category:
                filters['category'] = budget.category
            
            spending = Expense.objects.filter(**filters).aggregate(
                total_spent=models.Sum('amount')
            )
            total_spent = spending['total_spent'] or 0
            
            # Calculate thresholds
            threshold_90 = budget.amount * 0.9
            threshold_100 = budget.amount
            
            # Determine if we need to send an alert
            if total_spent >= threshold_100:
                subject = f"Budget Exceeded: {budget}"
                template = 'emails/budget_exceeded.html'
                text_template = 'emails/budget_exceeded.txt'
            elif total_spent >= threshold_90:
                subject = f"Budget Alert: {budget}"
                template = 'emails/budget_alert.html'
                text_template = 'emails/budget_alert.txt'
            else:
                continue
                
            # Prepare context and send email
            remaining = budget.amount - total_spent
            context = {
                'budget': budget,
                'total_spent': total_spent,
                'threshold_90': threshold_90,
                'threshold_100': threshold_100,
                'remaining': remaining,
                'percent_used': (total_spent / budget.amount) * 100,
                'site_name': 'Expense Tracker'
            }
            
            message = render_to_string(template, context)
            text_message = render_to_string(text_template, context)
            
            send_mail(
                subject=subject,
                message=text_message,
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[budget.user.email],
                fail_silently=False,
            )
            logger.info(f"Sent budget alert for budget ID: {budget.id}")
            
        except Exception as e:
            logger.error(f"Error processing budget {budget.id}: {str(e)}", exc_info=True)