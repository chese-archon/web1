import psycopg2
import select
import threading
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer #
#from .models import last_signal_message
import json


def listen_for_notifications():
    conn = psycopg2.connect(
        dbname=settings.DATABASES['data']['NAME'],
        user=settings.DATABASES['data']['USER'],
        password=settings.DATABASES['data']['PASSWORD'],
        host=settings.DATABASES['data']['HOST'],
        port=settings.DATABASES['data']['PORT']
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Подписка на уведомления
    cur.execute("LISTEN name_update;")
    cur.execute("LISTEN number_update;")
    
    print("Ожидание уведомлений...")
    channel_layer = get_channel_layer() #
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            #print('listen ', notify.channel)
            #print('pid ', notify.pid) # pid of proc
            notify = conn.notifies.pop(0)
            print(notify)
            """
            data = json.loads(notify.payload)  # Парсим JSON

            message = data["message"]
            old_value = data["old_value"]
            new_value = data["new_value"]
            """

            payload = notify.payload  # Получаем строку

            # Разбираем строку (разделитель — " | ")
            parts = payload.split(" | ")
            print(parts)
            message = parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3].split(": ")[1]  # Первое — сообщение table column id
            old_value = parts[4].split(": ")[1]  # Извлекаем старое значение
            new_value = parts[5].split(": ")[1]  # Извлекаем новое значение
            table = parts[1]
            column = parts[2]
            str_id = parts[3].split(": ")[1]

            print(f"{message}: было {old_value}, стало {new_value}")

            # Отправка в WebSocket через Django Channels
            async_to_sync(channel_layer.group_send)(
                "notifications_group",
                {
                    "type": "send_notification",
                    "message": message,
                    "old_value": old_value,
                    "new_value": new_value,
                    "table": table, 
                    "column": column,
                    "str_id": str_id, 
                }
            )

            """
            message = notify.payload
            last_signal_message = True#0
            if last_signal_message:
                print("Получено уведомление:", message)#notify.payload)
            
                print('notify ', notify)

                # Отправка в WebSocket через Django Channels
                async_to_sync(channel_layer.group_send)(
                    "notifications_group",
                {
                    "type": "send_notification",
                    "message": message,
                }
            )
            last_signal_message = True"
            """
