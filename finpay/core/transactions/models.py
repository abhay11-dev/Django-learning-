from django.db import models
from wallet.models import Wallet


class LedgerEntry(models.Model):

    ENTRY_TYPES = [
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="ledger_entries"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPES
    ) #CREDIT for money coming in, DEBIT for money going out

    reference = models.CharField(
        max_length=255,
        blank=True,
        null=True
    ) #optional field to store reference info like "Transfer to John" or "Transfer from Alice"

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.entry_type} - {self.amount}"