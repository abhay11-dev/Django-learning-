class Ledger(models.Model):

    debit_account = models.IntegerField()
    credit_account = models.IntegerField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)