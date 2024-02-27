from django.db import models
from user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.conf import settings
import json

class Collaborator(models.Model):
    note = models.ForeignKey("Notes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20,default="read_only")
    
    class Meta:
        db_table = 'collaborators'
    
class Notes(models.Model):
    title = models.CharField(max_length=254,null=True)
    description = models.TextField(null=True)
    color = models.CharField(max_length=50,null=True)
    remainder = models.DateTimeField(null=True)
    is_archive = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    Colaborator = models.ManyToManyField(User,related_name='collaborators',through=Collaborator)
    
    class Meta:
        db_table = 'Notes'


    def __str__(self):
        return self.title
    
class Labels(models.Model):
    name = models.CharField(max_length=50,null = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
   
@receiver(post_save, sender=Notes)
def set_reminder(instance, **kwargs):
    remainder = instance.remainder
    if remainder:
        day = remainder.day
        minute = remainder.minute
        hour = remainder.hour
        year = remainder.year
        month = remainder.month
        
        crontab, _ = CrontabSchedule.objects.get_or_create(minute=minute,
            hour=hour,
            day_of_month=day,
            month_of_year=month
        )
        
        task = PeriodicTask.objects.get_or_create(
            crontab=crontab,
            name=f"note-{instance.id}--user-{instance.user.id}",
            task = 'user.tasks.send_email_task',
            args = json.dumps([f'{instance.title}', 'Reminder for notes', settings.EMAIL_HOST_USER, [instance.user.email]])
        )