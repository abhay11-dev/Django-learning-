from django.db import migrations


def create_periodic_task(apps, schema_editor):
    IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')

    # Create or get interval (every 5 seconds)
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=5,
        period='seconds',
    )

    # Create or update periodic task
    PeriodicTask.objects.update_or_create(
        name='enqueue-pending-transactions',
        defaults={
            'interval': schedule,
            'task': 'apps.transactions.tasks.enqueue_pending_transactions',
            'enabled': True,
        }
    )


def delete_periodic_task(apps, schema_editor):
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')

    PeriodicTask.objects.filter(
        name='enqueue-pending-transactions'
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_deadlettertransaction'),
        ('django_celery_beat', '__latest__'),
    ]

    operations = [
        migrations.RunPython(create_periodic_task, delete_periodic_task),
    ]