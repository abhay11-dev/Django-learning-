from django.db import models


class LedgerEntry(models.Model):

    ENTRY_TYPES = [
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    ]

    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="ledger_entries"
    )

    transaction = models.ForeignKey(   
        "transactions.Transaction",
        on_delete=models.CASCADE,
        related_name="ledger_entries",
        null=True,  # Allow null for non-transactional entries (e.g. admin adjustments)
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: #inner class in models to define metadata, constraints and extra rules/metadata about the model itself
        constraints = [
            models.UniqueConstraint(
                fields=["wallet", "transaction", "entry_type"],
                name="unique_ledger_per_txn"
            )
        ]

    def __str__(self):
        return f"{self.wallet_id} | {self.entry_type} | {self.amount}"

