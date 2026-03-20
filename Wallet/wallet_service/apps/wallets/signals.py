from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Wallet
from apps.ledger.models import LedgerEntry

User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        wallet = Wallet.objects.create(user=instance, balance=1000)

        LedgerEntry.objects.create(
            wallet=wallet,
            amount=1000,
            entry_type="CREDIT"
        )