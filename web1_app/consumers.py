import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import last_signal_message

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications_group", self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        print('from websocket:', message)
        #if last_signal_message:
        await self.send(text_data=json.dumps({"message": message}))
        #else:
        #    print('no message from websocket')

