import psycopg2
import select
import threading
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer #
#from .models import last_signal_message


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
            message = notify.payload
            last_signal_message = 0
            if last_signal_message  != '':
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
