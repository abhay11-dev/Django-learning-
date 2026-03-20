from channels.generic.websocket import AsyncWebsocketConsumer
import json

class WalletConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f" Connected user {self.user_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_wallet_update(self, event):
        # Forward all data to JS directly
        await self.send(text_data=json.dumps({
            "type": "wallet.update",
            "wallet_id": event.get("wallet_id"),
            "user_id": event.get("user_id"),
            "balance": event.get("balance"),
            "transaction_id": event.get("transaction_id"),
            "status": event.get("status"),
        }))