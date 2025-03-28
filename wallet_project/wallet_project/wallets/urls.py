from django.urls import path
from .views import WalletBalanceView, WalletOperationView

urlpatterns = [
    path("api/v1/wallets/<uuid:wallet_id>/", WalletBalanceView.as_view(), name="wallet-balance"),
    path("api/v1/wallets/<uuid:wallet_id>/operation/", WalletOperationView.as_view(), name="wallet-operation"),
]
