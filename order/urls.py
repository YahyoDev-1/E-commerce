from django.urls import path
from .views import *

urlpatterns = [
    path('set-favorite/<slug:slug>/', set_favorite, name='set-favorite'),

    path('favorite_list/', FavoriteListView.as_view(), name='favorite_list'),

    path('set-cart/<slug:slug>', set_cart, name='set-cart'),

    path('my-cart/', CartView.as_view(), name='my-cart'),

    path('cart-increment/<int:pk>/', cart_inc, name='cart-increment'),

    path('cart-decrement/<int:pk>/', cart_dec, name='cart-decrement'),

    path('order/', OrderView.as_view(), name='order'),
]
