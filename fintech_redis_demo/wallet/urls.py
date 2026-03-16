from wallet.views import redis_test, get_balance

urlpatterns = [
    path("redis-test/", redis_test),
    path("balance/<int:user_id>/", get_balance),
]