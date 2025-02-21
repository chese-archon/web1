from django.apps import AppConfig
#added
import threading
from .notifications import listen_for_notifications

class Web1AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web1_app'

    def ready(self):
        # Запуск слушателя уведомлений в фоновом потоке
        thread = threading.Thread(target=listen_for_notifications)
        thread.daemon = True  # Чтобы поток закрывался при завершении основного потока
        thread.start()
