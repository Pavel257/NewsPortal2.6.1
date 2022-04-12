from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('authors/', AuthorList.as_view(), name='authors'),
    path('i18n/', include('django.conf.urls.i18n')),
    # Если вы используете классовые представления или дженерики, то нужно добавлять кэширование напрямую в urls.py
    # (в котором хранятся именно сами представления, а не основной urls.py из папки с settings.py).
    # время указывается в () нвпример, cache_page(60 - секунды *10) - будет 10 минут.
    # path('authors/', cache_page(60*10)(AuthorList.as_view()), name='authors'),
    path('category/', CategoryList.as_view(), name='category'),
    path('news/', NewsList.as_view(), name='news'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', AddNews.as_view(), name='news_create'),
    path('create/<int:pk>', ChangeNews.as_view(), name='news_update'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
    # path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    # path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
    path('subscribed/<int:news_category_id>', subscribe_me, name='subscribed'),
    path('index/', Index.as_view(), name='Index'),


]