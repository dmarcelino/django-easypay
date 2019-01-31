from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^notify', views.transaction_notification, name="transaction_notification"),
    url(r'^mbway_notify', views.mbway_notification, name="mbway_notification"),
]
