from django.db import models

class Wallet(models.Model):

    user_id = models.IntegerField()

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )