from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer


class WalletBalanceView(APIView):
    """Получение баланса кошелька"""
    def get(self, request, wallet_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id)
            return Response(WalletSerializer(wallet).data)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)


class WalletOperationView(APIView):
    """Пополнение и списание средств"""
    def post(self, request, wallet_id):
        operation_type = request.data.get("operation_type")
        amount = request.data.get("amount")

        if operation_type not in ["DEPOSIT", "WITHDRAW"]:
            return Response({"error": "Invalid operation type. Use 'DEPOSIT' or 'WITHDRAW'"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response({"error": "Invalid amount. Must be a positive number."},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                wallet = Wallet.objects.select_for_update().get(id=wallet_id)
            except Wallet.DoesNotExist:
                return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

            if operation_type == "WITHDRAW" and wallet.balance < amount:
                return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

            # Применяем изменение баланса
            wallet.balance += amount if operation_type == "DEPOSIT" else -amount
            wallet.save()

        return Response(WalletSerializer(wallet).data, status=status.HTTP_200_OK)
