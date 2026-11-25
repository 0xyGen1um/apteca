from django.contrib import admin
from .models import Category,Product,Inventory
admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','price','is_active','is_available','requires_prescription')
    list_filter=('category','is_active','requires_prescription')
    search_fields=('name',)
admin.site.register(Inventory)
