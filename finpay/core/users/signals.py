from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from wallet.models import Wallet


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


# signals are used to perform some action after a specific event occurs, in this case, after a User instance is created, we want to automatically create a Wallet for that user. 
# The post_save signal is sent after a model's save() method is called, and the receiver function listens for this signal and executes the code to create a Wallet when a new User is created.