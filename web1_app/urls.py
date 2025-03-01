from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.indexpage, name="home"),
    path("home/", views.indexpage, name="home"),
    path("<str:room_name>/", views.room, name="test"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)