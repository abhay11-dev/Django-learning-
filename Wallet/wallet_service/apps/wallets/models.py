from django.db import models
from django.db.models import Sum, Case, When, DecimalField
from django.conf import settings

class Wallet(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_balance_from_ledger(self):
        result = self.ledger_entries.aggregate(
            balance=Sum(
                Case(
                    When(entry_type="CREDIT", then="amount"),
                    When(entry_type="DEBIT", then=-1 * models.F("amount")),
                    output_field=DecimalField()
                )
            )
        )
        return result["balance"] or 0

    def __str__(self):
        return f"Wallet {self.id} | Balance: {self.balance}"