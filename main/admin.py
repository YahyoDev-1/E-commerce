from django.contrib import admin
from django.apps import apps

from main.models import *

# Register your models here.

admin.site.register(
    [Category, SubCategory, Seller, Property, Choice, Variant, Discount, Review, AdBanner]
)

class MediaInline(admin.StackedInline):
    model = Media
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [MediaInline]