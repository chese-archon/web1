import psycopg2
import select
import threading
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer #
#from .models import last_signal_message
import json


def parse(notify_playload):
    return

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
    cur.execute("LISTEN network_widget_update;")
    #cur.execute("LISTEN number_update;")
    
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
            
            