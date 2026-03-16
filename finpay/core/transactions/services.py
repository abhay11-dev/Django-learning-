from django.db import transaction
from decimal import Decimal

from wallet.models import Wallet
from .models import LedgerEntry


def transfer_money(sender_wallet, receiver_wallet, amount):

    amount = Decimal(amount)

    with transaction.atomic(): #ensure all operations succeed or fail together

        sender_wallet = Wallet.objects.select_for_update().get(id=sender_wallet.id)
        receiver_wallet = Wallet.objects.select_for_update().get(id=receiver_wallet.id)

        if sender_wallet.get_balance() < amount:
            raise Exception("Insufficient balance")

        LedgerEntry.objects.create(
            wallet=sender_wallet,
            amount=amount,
            entry_type="DEBIT",
            reference=f"Transfer to {receiver_wallet.user.username}"
        )

        LedgerEntry.objects.create(
            wallet=receiver_wallet,
            amount=amount,
            entry_type="CREDIT",
            reference=f"Transfer from {sender_wallet.user.username}"
        )