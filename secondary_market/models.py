from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=True)
    face_value = models.FloatField(null=False)
    expiry_date = models.DateField(null=False, blank=False)

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.TextField(max_length=250, blank=True, null=True)
    buyer_venmo_handle = models.TextField(max_length=50, blank=True, null=True)
    seller = models.TextField(max_length=250)
    seller_venmo_handle = models.TextField(max_length=50)
    exp_price = models.IntegerField(null=False)

