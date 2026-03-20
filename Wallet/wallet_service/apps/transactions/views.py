from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from decimal import Decimal, InvalidOperation
import json

from apps.wallets.models import Wallet
from apps.transactions.models import Transaction
from apps.transactions.tasks import process_transfer

User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
def transfer(request):
    """
    API endpoint for transferring money between wallets.
    Expected JSON payload:
    {
        "sender_id": <user_id>,
        "receiver_id": <user_id>,
        "amount": <decimal>
    }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    amount = data.get("amount")
    
    # Validation
    if not sender_id or not receiver_id or amount is None:
        return JsonResponse({"error": "Missing sender_id, receiver_id, or amount"}, status=400)
    
    try:
        sender = Wallet.objects.get(user_id=sender_id)
    except Wallet.DoesNotExist:
        return JsonResponse({"error": "Sender wallet not found"}, status=404)
    
    try:
        receiver = Wallet.objects.get(user_id=receiver_id)
    except Wallet.DoesNotExist:
        return JsonResponse({"error": "Receiver wallet not found"}, status=404)
    
    # Validation
    if sender.id == receiver.id:
        return JsonResponse({"error": "Cannot transfer to self"}, status=400)
    
    try:
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError
    except (InvalidOperation, TypeError, ValueError):
        return JsonResponse({"error": "Invalid amount"}, status=400)
    
    # Create transaction
    txn = Transaction.objects.create(
        sender=sender,
        receiver=receiver,
        amount=amount,
        status="PENDING"
    )
    
    # Async processing
    process_transfer.delay(txn.id)
    
    return JsonResponse({"transaction_id": txn.id, "status": "pending"})