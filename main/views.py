from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from main.models import Category, AdBanner
from users.models import User


# Create your views here.

class HomePageView(View):
    def get(self, request):
        if request.user.in_login():
            categories = Category.objects.all()
            banners = AdBanner.objects.all()
            context = {
                'categories': categories,
                'banners': banners,
            }

            return render(request, 'index.html', context)
        return render(request, 'index-without-auth.html')

class CategoryView(View):
    def get(self, request, slug):
        if request.user.in_login():
            category = get_object_or_404(Category, slug=slug)
            context = {
                'category': category,
            }
            return render(request, 'category.html', context)
        return redirect('login')
