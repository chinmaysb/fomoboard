from secondary_market.mailsender import send_mail
from django.shortcuts import render
from secondary_market.models import Transaction, Item, Payment, SendMail, inVenmoHook
from django.db.models import Count, Min, Sum, Avg
from django.db.models import Q
from secondary_market.app_logic import *
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
import venmo as vm
import random
import json
import datetime as dt
from secondary_market.csvexport import export_csv


def home(request, context=dict()):
    items_for_sale = dict()
    items_for_purchase = dict()

    for item in Item.objects.all().order_by('-transaction__tstamp'):
        if len(item.transaction_set.filter(Q(buyer=None))) > 0:
            q = dict()
            q['name'] = item.name
            q['description'] = item.description
            try:
                if (item.id not in items_for_sale.keys()):
                    q['buypx'] = \
                    item.transaction_set.filter(Q(buyer=None) & Q(cancelled=False)).aggregate(Min('exec_price'))[
                        'exec_price__min']
                    q['id'] = item.id
                    q['quantity'] = \
                    item.transaction_set.filter(Q(buyer=None) & Q(cancelled=False)).aggregate(Sum('quantity'))[
                        'quantity__sum']
                    q['icon'] = item.icon
                    items_for_sale[item.id] = q
            except:
                pass
        elif (len(item.transaction_set.filter(Q(seller=None))) > 0):
            q = dict()
            q['name'] = item.name
            q['description'] = item.description
            if (item.id not in items_for_purchase.keys()):
                try:
                    q['sellpx'] = \
                    item.transaction_set.filter(Q(seller=None) & Q(cancelled=False)).aggregate(Min('exec_price'))[
                        'exec_price__min']
                    q['id'] = item.id
                    q['quantity'] = \
                    item.transaction_set.filter(Q(seller=None) & Q(cancelled=False)).aggregate(Sum('quantity'))[
                        'quantity__sum']
                    # Add $1 spread
                    q['sellpx'] -= 1
                    q['icon'] = item.icon
                    items_for_purchase[item.id] = q
                except:
                    pass

    context['items_for_sale'] = list(items_for_sale.values())
    context['items_for_purchase'] = list(items_for_purchase.values())
    context['client_ip'] = request.META['REMOTE_ADDR']
    return render(request, 'index.html', context)


def executetransaction(request):
    context = dict()
    try:
        new_user = request.POST['user']
        new_user_venmo_handle = request.POST['user_venmo_handle']
        new_user_phone = request.POST['user_phone']
        buy_or_sell = request.POST['context']
        T = Transaction.objects.get(id=request.POST['txID'])
        if (buy_or_sell == "Buy"):
            T.buyer = new_user
            T.buyer_venmo_handle = new_user_venmo_handle
            T.buyer_phone = new_user_phone
            context[
                'TransactionMessage'] = "You have successfully bought an item! Please note down your transaction ID: " + str(
                T.id) + ". You will soon receive a Venmo charge request. You will receive details of the seller once you complete the request. The item will be returned to the pool if you don't complete the request within an hour."
        else:
            T.seller = new_user
            T.seller_venmo_handle = new_user_venmo_handle
            T.seller_phone = new_user_phone
            context[
                'TransactionMessage'] = "You have successfully sold an item! Please note down your transaction ID: " + str(
                T.id) + ". We have sent a Venmo charge request to the buyer. You will receive details of the buyer once they complete the request. The item will be returned to the pool if they don't complete the request within an hour."
        T.save()
        context['TransactionSuccess'] = True
        print(
            createEmail(T, new_user, "CBS Secondary Market Transaction ID#" + str(T.id), context['TransactionMessage']))
        return home(request, context)
    except Exception as e:
        pass


def dobuyoffer(request):
    return offerdispatcher("buy", request)


def doselloffer(request):
    return offerdispatcher("sell", request)


def dobuy(request):
    context = dict()
    context['item_to_buy'] = Transaction.objects.get(id=request.POST['item']).item
    context['transaction'] = Transaction.objects.get(id=request.POST['item'])
    # Add spread here
    context['transaction'].exec_price = context['transaction'].exec_price * context['transaction'].quantity
    return render(request, 'buy.html', context)


def checkitem(request):
    new_item_name = request.POST['name']
    new_item_description = request.POST['description']
    similar_items = dict()
    for item in Item.objects.all():
        new_similarity = similarity(item, new_item_description + new_item_name)
        if(len(similar_items)==0):
            similar_items[new_similarity] = item
        elif(new_similarity>min(similar_items.keys())):
            similar_items[new_similarity] = {'id':item.id, 'icon':item.icon, 'face_value': item.face_value, 'isStuGov':item.isStuGov,'name':item.name, 'description':item.description}
            if(len(similar_items)>3):
                del(similar_items[min(similar_items.keys())])
    similar_items = {k: v for k, v in similar_items.items() if k > 0.5}
    if(len(similar_items)==0):
        return additem(request)
    else:
        similar_items = list(similar_items.values())
        context = request.POST.copy()
        context['similar_items'] = similar_items
        return render(request, 'checkitem.html', context)

def additem(request):
    context = request
    context.POST = request.POST.copy()
    if(request.POST['item']=="-1"):
        new_name = request.POST["name"]
        new_description = request.POST["description"]
        new_face_value = request.POST["face_value"]
        new_expiry_date = request.POST["expiry_date"]
        new_icon = return_icon(new_description)
        if(new_expiry_date==None):
            new_expiry_date = dt.datetime.now() + dt.timedelta(days=15)
        new_isStuGov = (request.POST['isStuGov']=='on')
        I = Item(name=new_name, description=new_description, face_value=new_face_value, icon=new_icon, expiry_date=new_expiry_date, isStuGov=new_isStuGov)
        try:
            I.save()
            context.POST['offereditem'] = I
        except Exception as e:
            pass
    else:
        context.POST['offereditem'] = Item.objects.get(id=context.POST['item'])
    return addoffer(context)


def addoffer(request):
    context = dict()
    try:
        new_user = request.POST['user']
        new_user_venmo_handle = request.POST['user_venmo_handle']
        new_user_phone = request.POST['user_phone']
        new_quantity = request.POST['quantity']
        new_exec_price = request.POST['exec_price']
        buy_or_sell = request.POST['context']
        if type(request.POST['offereditem']) == int:
            item = Item.objects.get(id=request.POST['offereditem'].id)
        else:
            item = request.POST['offereditem']
        if (buy_or_sell == "Buy"):
            T = T = Transaction(item=item, id=generate_pk(), buyer=new_user, buyer_venmo_handle=new_user_venmo_handle,
                                buyer_phone=new_user_phone, exec_price=new_exec_price, quantity=new_quantity)
            context[
                'TransactionMessage'] = "You have successfully listed a buy order for an item. Please note down your transaction ID: " + str(
                T.id) + ". You will receive a Venmo charge request when a seller is matched against your order. You will receive details of the seller once you complete the request. The item will be returned to the pool if you don't complete the request within an hour of getting it."
        else:
            T = T = Transaction(item=item, id=generate_pk(), seller=new_user, seller_venmo_handle=new_user_venmo_handle,
                                seller_phone=new_user_phone, exec_price=new_exec_price, quantity=new_quantity)
            context[
                'TransactionMessage'] = "You have successfully listed a sell order for an item. Please note down your transaction ID: " + str(
                T.id) + ". Once we find a buyer, we will send a Venmo charge request to them. You will receive details of the buyer once they complete the request. The item will be returned to the pool if they don't complete the request within an hour."
        T.save()
        context['TransactionSuccess'] = True
        print(
            createEmail(T, new_user, "CBS Secondary Market Transaction ID#" + str(T.id), context['TransactionMessage']))
        return home(request, context)
    except Exception as e:
        context['TransactionMessage'] += str(e)
        return render(request, request.META.get('HTTP_REFERER', '/'), context)
        pass


def show_sell_page(request):
    context = dict()
    context['context'] = "Sell"
    context['items'] = Item.objects.all()
    return render(request, 'item.html', context)


def show_buy_page(request):
    context = dict()
    context['context'] = "Buy"
    context['items'] = Item.objects.all()
    return render(request, 'item.html', context)


def buydispatcher(request):
    return dispatcher("buy", request)


def selldispatcher(request):
    return dispatcher("sell", request)


def docancel(request):
    context = dict()
    txid_to_cancel = request.POST['txid_cancel']
    email_to_cancel = request.POST['email_cancel']

    if (Transaction.objects.filter(
            Q(id=txid_to_cancel) & Q(buyer=email_to_cancel) & Q(seller=None) & Q(cancelled=False)).count() > 0):
        try:
            T = Transaction.objects.filter(
                Q(id=txid_to_cancel) & Q(buyer=email_to_cancel) & Q(seller=None) & Q(cancelled=False))[0]
            T.cancelled = True
            T.save()
            context['TransactionSuccess'] = True
            context['TransactionMessage'] = "You have successfully cancelled the listing with ID " + str(T.id) + "."
            createEmail(T, T.buyer, "CBS Secondary Market Transaction ID#" + str(T.id), context['TransactionMessage'])
            return home(request, context)
        except Exception as e:
            print(e)

    elif (Transaction.objects.filter(
            Q(id=txid_to_cancel) & Q(seller=email_to_cancel) & Q(buyer=None) & Q(cancelled=False)).count() > 0):
        try:
            T = Transaction.objects.filter(
                Q(id=txid_to_cancel) & Q(seller=email_to_cancel) & Q(buyer=None) & Q(cancelled=False))[0]
            T.cancelled = True
            T.save()
            context['TransactionSuccess'] = True
            context['TransactionMessage'] = "You have successfully cancelled the listing with ID " + str(T.id) + "."
            createEmail(T, T.seller, "CBS Secondary Market Transaction ID#" + str(T.id), context['TransactionMessage'])
            return home(request, context)
        except Exception as e:
            print(e)
            pass

    context['TransactionSuccess'] = False
    context[
        'TransactionMessage'] = "Could not find that transaction (or it's already been cancelled) - please try again!"
    return home(request, context)


def dodispute(request):
    context = dict()
    txid_to_cancel = request.POST['txid_dispute']
    email_to_cancel = request.POST['email_dispute']

    if (Transaction.objects.filter(Q(id=txid_to_cancel) & Q(buyer=email_to_cancel) & Q(cancelled=False)).count() > 0):
        try:
            T = Transaction.objects.filter(Q(id=txid_to_cancel) & Q(buyer=email_to_cancel) & Q(cancelled=False))[0]
            context['TransactionSuccess'] = True
            context[
                'TransactionMessage'] = "You have successfully raised a dispute for the transaction bearing ID " + str(
                T.id) + ". Someone from our team will be in touch shortly."
            createEmail(T, "self", "CBS Secondary Market Transaction ID#" + str(T.id),
                        context['TransactionMessage'] + request.POST['dispute'])
            return home(request, context)
        except Exception as e:
            print(e)

    elif (Transaction.objects.filter(
            Q(id=txid_to_cancel) & Q(seller=email_to_cancel) & Q(cancelled=False)).count() > 0):
        try:
            T = Transaction.objects.filter(Q(id=txid_to_cancel) & Q(seller=email_to_cancel) & Q(cancelled=False))[0]
            context['TransactionSuccess'] = True
            context[
                'TransactionMessage'] = "You have successfully raised a dispute for the transaction bearing ID " + str(
                T.id) + ". Someone from our team will be in touch shortly."
            createEmail(T, "self", "CBS Secondary Market Transaction ID#" + str(T.id),
                        context['TransactionMessage'] + request.POST['dispute'])
            return home(request, context)
        except Exception as e:
            print(e)
            pass

    context['TransactionSuccess'] = False
    context['TransactionMessage'] = "Could not find that transaction - please try again!"
    return home(request, context)
