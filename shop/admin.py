from django.contrib import admin
from .models import *


class ImageInLine(admin.TabularInline):
    model = Image
    extra = 0

class FeatureInLine(admin.TabularInline):
    model = ProductFeature
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
     
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'new_price', 'created', 'updated']
    list_filter = ['created', 'updated']
    prepopulated_fields = {'slug': ('name',)} 
    inlines = [ImageInLine,FeatureInLine]