from multiprocessing import context
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from main.models import Product
from .models import Favorite, CartItem, Order


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
    path = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated and request.user.confirmed:
        product = get_object_or_404(Product, slug=slug)
        if Favorite.objects.filter(user=request.user, product=product).exists():
            Favorite.objects.filter(user=request.user, product=product).delete()
            return redirect(path)
        else:
            Favorite.objects.create(user=request.user, product=product)
            return redirect(path)
    return redirect('login')


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            cart_items = CartItem.objects.filter(user=request.user)
            context = {
                'cart_items': cart_items,
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


def cart_inc(request, pk):
    with transaction.atomic():  # Barcha amallar muvaffaqiyatli bo'lishi shart
        # select_for_update() boshqa userlar bu qatorni o'zgartirishini kutdirib turadi
        cart_item = CartItem.objects.select_for_update().get(id=pk, user=request.user)

        if cart_item.amount < cart_item.product.amount:
            cart_item.amount += 1
            cart_item.save()
        else:
            messages.warning(request, "Mahsulot yetarli emas")

    return redirect('my-cart')


def cart_dec(request, pk):
    if request.user.is_authenticated and request.user.confirmed:
        cart_item = get_object_or_404(CartItem, user=request.user, id=pk)
        if cart_item.amount == 1 or request.GET.get('delete') == '1':
            CartItem.objects.filter(user=request.user, id=pk).delete()
        else:
            cart_item.amount -= 1
            cart_item.save()
        return redirect('my-cart')
    return redirect('login')

class OrderView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            orders = Order.objects.filter(user=request.user)
            context = {
                'orders': orders,
            }
            return render(request, 'order-payment.html', context)
        return redirect('login')