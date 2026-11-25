from django.db import models
from django.db.models import Q

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    age_limit = models.PositiveSmallIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    requires_prescription = models.BooleanField(default=False)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(price__gte=0),name='product_price_nonnegative')]
    def __str__(self): return self.name
    def delete(self,*args,**kwargs):
        if self.orderitem_set.exists():
            self.is_active=False; self.save(update_fields=['is_active'])
        else: super().delete(*args,**kwargs)

class Inventory(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='inventory')
    stock_quantity = models.PositiveIntegerField(default=0)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(stock_quantity__gte=0),name='stock_nonnegative')]
