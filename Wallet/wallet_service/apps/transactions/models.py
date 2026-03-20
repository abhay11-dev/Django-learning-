from ast import For

from django.db import models


class Transaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"), 
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    sender = models.ForeignKey(
        "wallets.Wallet",
        related_name="sent_transactions",
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        "wallets.Wallet",
        related_name="received_transactions",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    failure_reason = models.TextField(null=True, blank=True)  #Add in future for better error handling and debugging

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_dlq = models.BooleanField(default=False)  # Flag to mark if this txn is in Dead Letter Queue

    def __str__(self):
        return f"Txn {self.id} | {self.sender_id} → {self.receiver_id} | {self.amount} | {self.status}"
    


class DeadLetterTransaction(models.Model): #DLT is for system failures not business logic failures. 
    transaction = models.ForeignKey("transactions.Transaction", on_delete=models.CASCADE)
    error_message = models.TextField()
    failed_at = models.DateTimeField(auto_now_add=True)
    retry_count = models.IntegerField(default=0)