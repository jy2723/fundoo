from celery import shared_task
from django.core.mail import send_mail


@shared_task
def celery_send_email(email,token):
    return success

    

@shared_task
def send_email_task(subject, message,from_mail, recipient_list):

    send_mail(subject, message, from_mail, recipient_list)
        
    
@shared_task
def add():
    return 10 + 10