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
        old_value = event["old_value"]
        new_value = event["new_value"]
        table = event["table"]
        column = event["column"]
        str_id = event["str_id"]
        print('from websocket:', message, old_value, new_value)
        #if last_signal_message:
        await self.send(text_data=json.dumps({"message": message,
                                              "old_value": old_value,
                                              "new_value": new_value,
                                              "table": table,
                                              "column": column,
                                              "str_id": str_id 
                                              }))
        #else:
        #    print('no message from websocket')

