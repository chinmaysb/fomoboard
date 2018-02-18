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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^sell', views.sell, name='sell'),
    url(r'^dosellitem', views.dosellitem, name='dosellitem'),
    url(r'^doselloffer', views.doselloffer, name='doselloffer'),
    url(r'^dobuyitem', views.dobuyitem, name='dobuyitem'),
    url(r'^dobuy', views.dobuy, name='dobuy'),
    url(r'^verifypayment', views.verifypayment, name='verifypayment'),
]