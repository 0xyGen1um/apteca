from django.conf import settings
from django.db import models
from enums import PrescriptionStatus

class Prescription(models.Model):
    order=models.ForeignKey('orders.Order',on_delete=models.CASCADE,related_name='prescriptions')
    product=models.ForeignKey('catalog.Product',on_delete=models.PROTECT)
    image=models.ImageField(upload_to='prescriptions/')
    status=models.CharField(max_length=10,choices=PrescriptionStatus.choices,default=PrescriptionStatus.PENDING)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    reviewed_at=models.DateTimeField(null=True,blank=True)
    reviewed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    rejection_reason=models.TextField(blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['order','product'],name='unique_prescription_product')]
