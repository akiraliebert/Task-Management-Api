from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_task_reminder(task_id, user_email):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {"status": "not_found", "task_id": task_id}
    subject = f"Reminder: {task.title}"
    body = f"Task: {task.title}\n\n{task.description or ''}\n\nDue: {task.due_date}"
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
    return {"status": "sent", "task_id": task_id}

@shared_task
def cleanup_completed_tasks(days=30):
    cutoff = timezone.now() - timedelta(days=days)
    qs = Task.objects.filter(status="done", updated_at__lt=cutoff)
    count = qs.count()
    qs.delete()
    return {"deleted": count}
