from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from wallet.models import Wallet
from .services import transfer_money


class TransferView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        receiver_id = request.data.get("receiver_id")
        amount = request.data.get("amount")

        if not receiver_id or not amount:
            return Response(
                {"error": "receiver_id and amount required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        sender_wallet = request.user.wallet

        try:
            receiver_wallet = Wallet.objects.get(id=receiver_id)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Receiver wallet not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            transfer_money(sender_wallet, receiver_wallet, amount)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "status": "SUCCESS",
            "amount": amount
        })