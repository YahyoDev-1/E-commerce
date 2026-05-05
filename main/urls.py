from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),

    path('products/', ProductsView.as_view(), name='products'),

    path('products/<slug:slug>/', ProductDetailsView.as_view(), name='product-details'),

    path('add-review/<slug:slug>/', AddReviewView.as_view(), name='add-review'),

]