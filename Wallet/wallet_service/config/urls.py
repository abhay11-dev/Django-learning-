from django.contrib import admin
from django.urls import include, path
from apps.wallets.views import ws_test, wallet_balance_api, transaction_activity_api
from apps.wallets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ws-test/', ws_test, name='ws_test'),
    path("wallets/", views.wallet_dashboard, name="wallet_dashboard"),
    path("api/wallet-balances/", wallet_balance_api, name="wallet_balance_api"),
    path("api/transactions/activity/", transaction_activity_api, name="transaction_activity_api"),
    path("api/", include("apps.transactions.urls")),  # Include transaction URLs
]