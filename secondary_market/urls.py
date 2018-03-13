"""secondary_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url
from secondary_market import views
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^sell$', views.show_sell_page, name='sell'),
    url(r'^buy$', views.show_buy_page, name='buy'),
    url(r'^buydispatcher', views.buydispatcher, name='buydispatcher'),
    url(r'^selldispatcher', views.selldispatcher, name='selldispatcher'),
    url(r'^checkitem', views.checkitem, name='checkitem'),
    url(r'^dobuy$', views.dobuyoffer, name='dobuy'),
    url(r'^dosell$', views.doselloffer, name='dosell'),
    url(r'^dobuyoffer', views.dobuyoffer, name='dobuyoffer'),
    url(r'^doselloffer', views.doselloffer, name='doselloffer'),
    url(r'^executetransaction', views.executetransaction, name='executetransaction'),
    url(r'^additem', views.additem, name='additem'),
    url(r'^addoffer$', views.addoffer, name='addoffer'),
    url(r'^docancel', views.docancel, name='docancel'),
    url(r'^dodispute', views.dodispute, name='dodispute'),
    url(r'^verifypayment', csrf_exempt(views.verifypayment), name='verifypayment'),

]
