from __future__ import unicode_literals

from django.dispatch import Signal


notification_received = Signal(providing_args=["notification"])
