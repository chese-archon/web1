import psycopg2
import select
import threading
from django.conf import settings

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

    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print("Получено уведомление:", notify.payload)
