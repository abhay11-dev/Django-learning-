from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ["id", "user", "created_at", "balance"]

    def get_balance(self, obj):
        return obj.get_balance()