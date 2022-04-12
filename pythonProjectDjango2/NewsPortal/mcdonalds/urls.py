from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view()),
    path('new/', NewOrderView.as_view(), name='new_order'),
    path('take/<int:oid>', take_order, name='take_order'),
    # модуль Д7 - таски и редис
    path('main/', ProductView.as_view(), name='mcd'),
]