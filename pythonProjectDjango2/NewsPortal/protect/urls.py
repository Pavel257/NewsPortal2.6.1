from django.urls import path, include
from .views import IndexView

# перенаправляемся на единственное представление IndexView, которое описано в соответствующем файле views.py
urlpatterns = [
    path('', IndexView.as_view()),
    path('i18n/', include('django.conf.urls.i18n')),
]