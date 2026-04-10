from rest_framework.views import APIView
from rest_framework.response import Response

class SendPayment(APIView):

    def post(self, request):

        sender = request.data["sender"]
        receiver = request.data["receiver"]
        amount = request.data["amount"]

        return Response({
            "status": "payment_success",
            "amount": amount
        })