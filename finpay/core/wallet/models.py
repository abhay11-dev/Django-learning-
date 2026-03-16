from django.db import models
from django.db.models import Sum


class Wallet(models.Model):

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_balance(self):

        from transactions.models import LedgerEntry  #import here to avoid circular import issues
        
        """ A circular import happens when two or more Python modules depend on each other while loading, creating a loop that Python cannot resolve during import time.
            In Python, modules are executed top → bottom during import. If module A imports B, and B imports A before A finishes loading, Python sees a partially initialized module and throws an error.
        """         

        credits = LedgerEntry.objects.filter(
            wallet=self,
            entry_type="CREDIT"
        ).aggregate(total=Sum("amount"))["total"] or 0

        debits = LedgerEntry.objects.filter(
            wallet=self,
            entry_type="DEBIT"
        ).aggregate(total=Sum("amount"))["total"] or 0

        return credits - debits