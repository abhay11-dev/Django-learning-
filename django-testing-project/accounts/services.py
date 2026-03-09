from .models import Wallet,Transaction

def add_money(user,amount):

    wallet = Wallet.objects.get(user=user)

    wallet.balance += amount
    wallet.save()

    return wallet


def transfer_money(sender,receiver,amount):

    sender_wallet = Wallet.objects.get(user=sender)
    receiver_wallet = Wallet.objects.get(user=receiver)

    if sender_wallet.balance < amount:
        raise Exception("Insufficient balance")

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    sender_wallet.save()
    receiver_wallet.save()

    Transaction.objects.create(
        sender=sender,
        receiver=receiver,
        amount=amount
    )