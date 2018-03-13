from django.db import models
from django.contrib.auth.models import User
import datetime as dt
import random, string


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, blank=False)
    isStuGov = models.BooleanField(null=False, default=False)
    description = models.TextField(max_length=500, blank=True)
    face_value = models.FloatField(null=False)
    expiry_date = models.DateField(null=False, blank=False, default=(dt.datetime.now() + dt.timedelta(days=14)))
    icon = models.TextField(max_length=50, blank=True, default="fa-certificate")


class inVenmoHook(models.Model):
    json_text = models.TextField(max_length=200000, blank=True, null=True)


class Transaction(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=True, default=1)
    buyer = models.TextField(max_length=250, blank=True, null=True)
    buyer_phone = models.TextField(max_length=10, blank=True, null=True)
    buyer_venmo_handle = models.TextField(max_length=100, blank=True, null=True)
    seller = models.TextField(max_length=250, blank=True, null=True)
    seller_phone = models.TextField(max_length=10, blank=True, null=True)
    seller_venmo_handle = models.TextField(max_length=100, blank=True, null=True)
    exec_price = models.IntegerField(null=False, blank=True, default=0)  # This is the unit price, to be treated as such
    reserve_price = models.IntegerField(null=False, blank=True, default=9999)
    decay_rate = models.IntegerField(null=False, blank=True, default=0)
    pickup_location = models.TextField(max_length=500, blank=True, null=False, default="On-campus")
    email_sent = models.BooleanField(null=False, blank=False, default=False)
    email_tries = models.IntegerField(null=False, blank=True, default=0)
    payment_in_completed = models.BooleanField(null=False, blank=False, default=False)
    payment_out_completed = models.BooleanField(null=False, blank=False, default=False)
    payment_tries = models.IntegerField(null=False, blank=True, default=0)
    cancelled = models.BooleanField(null=False, blank=False, default=False)
    tstamp = models.DateTimeField(auto_now=True)

    def _get_total_px(self):
        return self.quantity * self.exec_price

    total_price = property(_get_total_px)


class Payment(models.Model):
    txid = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    byVenmo = models.BooleanField(null=False, blank=False, default=True)
    receipient = models.TextField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(null=False, blank=True, default=9999)
    complete = models.BooleanField(null=False, blank=False, default=False)
    tstamp = models.DateTimeField(auto_now=True)


class SendMail(models.Model):
    txid = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    to = models.TextField(max_length=250, blank=True, null=True)
    subject = models.TextField(max_length=250, blank=True, null=True)
    body = models.TextField(max_length=25000, blank=True, null=True)
    complete = models.BooleanField(null=False, blank=False, default=False)
    tstamp = models.DateTimeField(auto_now=True)
