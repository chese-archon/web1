import json
from django.http import JsonResponse

from .models import Data


#data = Data.objects.using('data').all()

class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/api/notification_closed/" and request.method == "POST":
            data = json.loads(request.body) # message in str format
            print("Окно закрыто:", data)
            data2 = Data.objects.using('data').all()
            for i in data2:
                i.refresh_from_db()
            print("i.refresh_from_db() END")
            return JsonResponse({"status": "ok"})       
        response = self.get_response(request)
        return response
