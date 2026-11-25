from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from .models import Category,Product

def home(request):
    qs=Product.objects.filter(is_active=True,is_available=True).select_related('category','inventory')
    if request.GET.get('q'): qs=qs.filter(Q(name__icontains=request.GET['q'])|Q(description__icontains=request.GET['q']))
    if request.GET.get('category'): qs=qs.filter(category_id=request.GET['category'])
    return render(request,'catalog/home.html',{'products':qs,'categories':Category.objects.all(),'query':request.GET.get('q','')})

def product(request,pk): return render(request,'catalog/product.html',{'product':get_object_or_404(Product.objects.select_related('inventory','category'),pk=pk,is_active=True)})
