from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^notify', views.generic_notification, name="generic_notification"),
    url(r'^authorisation_notify', views.authorisation_notification, name="authorisation_notification"),
    url(r'^transaction_notify', views.transaction_notification, name="transaction_notification"),
    url(r'^mbway_notify', views.mbway_notification, name="mbway_notification"),
]
