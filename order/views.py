from multiprocessing import context

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from main.models import Product
from .models import Favorite, CartItem


# Create your views here.

class FavoriteListView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            favorites = Favorite.objects.filter(user=request.user)
            context = {
                'favorites': favorites
            }
            return render(request, 'favorite_list.html', context)
        return redirect('login')


def set_favorite(request, slug):
    if request.user.is_authenticated and request.user.confirmed:
        product = get_object_or_404(Product, slug=slug)
        if Favorite.objects.filter(user=request.user, product=product).exists():
            Favorite.objects.filter(user=request.user, product=product).delete()
            return redirect('product-details', slug=slug)
        else:
            Favorite.objects.create(user=request.user, product=product)
            return redirect('favorite_list')
    return redirect('login')


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            cart_items = CartItem.objects.filter(user=request.user)
            context = {
                'cart_items': cart_items
            }
            return render(request, 'cart.html', context)
        return redirect('login')


def set_cart(request, slug):
    if request.user.is_authenticated and request.user.confirmed:
        product = get_object_or_404(Product, slug=slug)
        if CartItem.objects.filter(user=request.user, product=product).exists():
            cart_item = get_object_or_404(CartItem, user=request.user, product=product)
            cart_item.amount += 1
            cart_item.save()
        else:
            CartItem.objects.create(user=request.user, product=product)
        return redirect('my-cart')
    return redirect('login')