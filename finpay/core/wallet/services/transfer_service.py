from django.db import transaction
from wallet.models import Wallet
from transactions.models import LedgerEntry


def transfer_money(sender_wallet_id, receiver_wallet_id, amount):

    with transaction.atomic(): #Atomic transaction to ensure data integrity

        sender_wallet = Wallet.objects.select_for_update().get( #Lock the sender's wallet for update, to prevent race condiditon, else other transfer can also read the same balance and cause negative balance but still pass negative case as reading at same time, both will read same balance and pass negative case.
            id=sender_wallet_id
        )

        receiver_wallet = Wallet.objects.select_for_update().get( #Lock the receiver's wallet for update to prevent race condition.
            id=receiver_wallet_id
        )

        if sender_wallet.get_balance() < amount:
            raise Exception("Insufficient funds")

        # debit sender
        LedgerEntry.objects.create(
            wallet=sender_wallet,
            amount=amount,
            entry_type="DEBIT",
            reference=f"Transfer to {receiver_wallet.user.username}"
        )

        # credit receiver
        LedgerEntry.objects.create(
            wallet=receiver_wallet,
            amount=amount,
            entry_type="CREDIT",
            reference=f"Transfer from {sender_wallet.user.username}"
        )

        return "Transfer Successful"