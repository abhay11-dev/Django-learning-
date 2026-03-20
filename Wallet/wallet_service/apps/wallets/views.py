from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Wallet
from apps.transactions.models import Transaction
from apps.ledger.models import LedgerEntry
import json
from datetime import datetime

User = get_user_model()

def wallet_dashboard(request):
    return render(request, "wallets.html")

def wallet_balance_api(request):
    """API endpoint to fetch all wallet balances dynamically"""
    try:
        # Get all non-system wallets, sorted by user ID
        wallets = Wallet.objects.select_related('user').exclude(
            user__username='SYSTEM'
        ).order_by('user__id')
        
        data = {
            'wallets': [
                {
                    'user_id': wallet.user.id,
                    'username': wallet.user.username,
                    'balance': float(wallet.balance),
                }
                for wallet in wallets
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def transaction_activity_api(request):
    """API endpoint to fetch recent transactions for live activity feed"""
    try:
        # Get last 50 transactions, sorted by most recent
        transactions = Transaction.objects.select_related(
            'sender__user', 'receiver__user'
        ).order_by('-created_at')[:50]
        
        data = {
            'transactions': [
                {
                    'id': txn.id,
                    'sender': txn.sender.user.username if txn.sender else 'SYSTEM',
                    'receiver': txn.receiver.user.username if txn.receiver else 'SYSTEM',
                    'amount': float(txn.amount),
                    'status': txn.status,
                    'created_at': txn.created_at.isoformat() if hasattr(txn, 'created_at') else datetime.now().isoformat(),
                }
                for txn in transactions
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ws_test(request):
    from django.http import HttpResponse
    return HttpResponse("Websocket test works!")