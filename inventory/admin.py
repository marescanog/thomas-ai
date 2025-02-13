from django.contrib import admin
from .models import Products  
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'class_index', 'class_label_name', 'product_name', 'product_type', 'alcohol_volume', 'product_type')
    search_fields = ('class_label_name', 'product_type', 'made_in', 'made_by', 'sugar_content', 'varietal')
