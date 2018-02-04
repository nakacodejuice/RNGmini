"""RNGmini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import ImpersonalRNG.views
import SoapLikeRNG.views
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from SoapLikeRNG.views import app, DataExchange

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^say_hello/', DjangoView.as_view(
        services=[DataExchange], tns='http://www.dataexchange.org', name='DataExchangeSoapBinding',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    url(r'^say_hello_not_cached/', DjangoView.as_view(
        services=[DataExchange], tns='http://www.dataexchange.org', name='DataExchangeSoapBinding',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11(),
        cache_wsdl=False)),
    url(r'^api/', DjangoView.as_view(application=app)),
]
