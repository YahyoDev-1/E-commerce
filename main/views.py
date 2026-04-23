from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from main.models import Category, AdBanner, Product, SubCategory


# Create your views here.

class HomePageView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
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
        if request.user.is_authenticated and request.user.confirmed:
            category = get_object_or_404(Category, slug=slug)
            sub_categories = category.subcategory_set.filter(category=category).order_by('-image')
            context = {
                'category': category,
                'sub_categories': sub_categories,
            }
            return render(request, 'category.html', context)
        return redirect('login')


class ProductsView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.confirmed:
            products = Product.objects.all()

            query_view = request.GET.get('view')

            query_sub = request.GET.get('sub-category')
            sub_category = None
            if query_sub:
                sub_category = get_object_or_404(SubCategory, slug=query_sub)
                products = products.filter(sub_category=sub_category)

            context = {
                'products': products,
                'query_sub': query_sub,
                'sub_category': sub_category,
            }

            if query_view.lower() == 'large':
                return render(request, 'products-large.html', context)
            return render(request, 'products-grid.html', context)
        return redirect('login')
