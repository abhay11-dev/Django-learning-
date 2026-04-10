from celery import shared_task
from django.db import transaction as db_transaction
from django.db.models import Sum, F, Case, When, DecimalField
from apps.transactions.models import NotificationStatus, Transaction, DeadLetterTransaction
from apps.wallets.models import Wallet
from apps.ledger.models import LedgerEntry
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.transactions.alerts import send_failure_alert

logger = logging.getLogger(__name__)


def send_ws_event(sender, receiver, txn):
    """
    Send WebSocket event to update wallets. 
    """
    try:
        channel_layer = get_channel_layer()
        for w in [sender, receiver]:
            async_to_sync(channel_layer.group_send)(
                f"user_{w.user.id}",
                {
                    "type": "send_wallet_update",
                    "wallet_id": w.id,
                    "user_id": w.user.id,
                    "balance": str(w.balance),
                    "transaction_id": txn.id,
                    "status": txn.status,
                }
            )
    except Exception as e:
        logger.error(f"WebSocket send failed for txn {txn.id}: {e}")


def compute_balance(wallet):
    """
    Compute balance from ledger (source of truth).
    """
    result = LedgerEntry.objects.filter(wallet=wallet).aggregate(
        balance=Sum(
            Case(
                When(entry_type="CREDIT", then=F("amount")),
                When(entry_type="DEBIT", then=-F("amount")),
                output_field=DecimalField()
            )
        )
    )
    return result["balance"] or 0


@shared_task(bind=True, max_retries=3)
def process_transfer(self, transaction_id):
    try:
        with db_transaction.atomic():
            # Idempotency guard: only PENDING txn
            updated = Transaction.objects.filter(
                id=transaction_id,
                status="PENDING"
            ).update(status="PROCESSING")

            if not updated:
                logger.info(f"Txn {transaction_id} already processed/skipped")
                return

            # Lock transaction row
            txn = Transaction.objects.select_for_update().get(id=transaction_id)

            # Lock wallets in a consistent order to prevent deadlocks
            wallet_ids = sorted([txn.sender_id, txn.receiver_id])
            wallets = Wallet.objects.select_for_update().filter(id__in=wallet_ids)
            wallet_map = {w.id: w for w in wallets}

            sender = wallet_map[txn.sender_id]
            receiver = wallet_map[txn.receiver_id]

            # Check sender balance from ledger (source of truth)
            sender_balance = compute_balance(sender)
            if sender_balance < txn.amount:
                txn.status = "FAILED"
                txn.failure_reason = "Insufficient balance"
                txn.save(update_fields=["status", "failure_reason"])
                logger.warning(f"Txn {txn.id} failed: insufficient balance")
                return

        

            # Create ledger entries safely (idempotent)
            debit_entry, created_debit = LedgerEntry.objects.get_or_create(
                wallet=sender,
                transaction=txn,
                entry_type="DEBIT",
                defaults={"amount": txn.amount},
            )
            credit_entry, created_credit = LedgerEntry.objects.get_or_create(
                wallet=receiver,
                transaction=txn,
                entry_type="CREDIT",
                defaults={"amount": txn.amount},
            )

            if not (created_debit and created_credit):
                logger.warning(f"Txn {txn.id}: duplicate ledger prevented")

            # Update wallet balances (always from ledger)
            sender.balance = compute_balance(sender)
            receiver.balance = compute_balance(receiver)
            sender.save(update_fields=["balance"])
            receiver.save(update_fields=["balance"])

            # Mark transaction success
            txn.status = "SUCCESS"
            txn.save(update_fields=["status"])

        # WebSocket event after commit
        send_ws_event(sender, receiver, txn)
        logger.info(f"Txn {txn.id} processed successfully")

    except Exception as e:
        # Retry logic with DLQ on max retries
        txn = Transaction.objects.filter(id=transaction_id).first()
        if self.request.retries >= self.max_retries:
            if txn:
                txn.status = "FAILED"
                txn.failure_reason = str(e)
                txn.is_dlq = True
                txn.save()

                DeadLetterTransaction.objects.create(
                    transaction=txn,
                    error_message=str(e)
                )
                send_failure_alert(txn, str(e))
            return

        # Retry after short delay
        raise self.retry(exc=e, countdown=5)
    




@shared_task
def enqueue_pending_transactions():
    pending_txns = Transaction.objects.filter(status="PENDING")
    
    for txn in pending_txns:
        process_transfer.delay(txn.id)

    return f"{pending_txns.count()} transactions enqueued"


@shared_task
def send_notification(txn_id):
    try:
        websocket_send(txn_id)

        NotificationStatus.objects.update_or_create(
            transaction_id=txn_id,
            defaults={"is_delivered": True}
        )

    except Exception as e:
        NotificationStatus.objects.update_or_create(
            transaction_id=txn_id,
            defaults={
                "is_delivered": False,
                "retry_count": F("retry_count") + 1
            }
        )

def retry_notifications():
    failed = NotificationStatus.objects.filter(
        is_delivered=False,
        retry_count__lt=5
    )

    for item in failed:
        send_notification(item.transaction_id)