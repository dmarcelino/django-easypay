from __future__ import unicode_literals

from django.dispatch import Signal


generic_notification = Signal(providing_args=["notification"])
authorisation_notification = Signal(providing_args=["notification"])
transaction_notification = Signal(providing_args=["notification"])

mbway_notification = Signal(providing_args=["notification"])
