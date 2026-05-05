from django.urls import path
from .views import *

urlpatterns = [
    path('set-favorite/<slug:slug>/', set_favorite, name='set-favorite'),

    path('favorite_list/', FavoriteListView.as_view(), name='favorite_list'),

    path('set-cart/<slug:slug>', set_cart, name='set-cart'),

    path('my-cart/', CartView.as_view(), name='my-cart'),
]
