from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Post  # Replace YourModel with the actual name of your model

@receiver(post_save, sender=Post)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        subject = 'A new post has been created'
        message = 'A new post has been created. Check it out now!\n\n' + "title:"+instance.title + '\n\n' + instance.body + '\n\n' 
        recipient_list = [instance.author.email]  # Specify the recipient email addresses
        send_mail(subject, message,settings.EMAIL_HOST_USER , recipient_list)
