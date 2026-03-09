from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)

class Transaction(models.Model):

    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="received")

    amount = models.DecimalField(max_digits=10,decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)