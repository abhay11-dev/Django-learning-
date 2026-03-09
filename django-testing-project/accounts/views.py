from rest_framework.views import APIView
from rest_framework.response import Response
from .services import add_money

class AddMoneyView(APIView):

    def post(self,request):

        amount = request.data.get("amount")

        wallet = add_money(request.user,amount)

        return Response({"balance":wallet.balance})