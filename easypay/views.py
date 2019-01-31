from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

from .api import TransactionNotification, MbwayNotification
from .signals import notification_received


log = logging.getLogger(__name__)


# Create your views here.
@require_POST
@csrf_exempt
def transaction_notification(request):
    """
    Transaction Notification endpoint
    :param request:
    :return:
    """
    log.info("transaction_notification, Easypay incoming POST data: \n%s", request.body)

    encoding = request.POST.get('charset', 'utf-8')
    data = json.loads(request.body.decode(encoding))

    notification = TransactionNotification(data)

    log.debug("Easypay notification: %s", vars(notification))

    notification_received.send(sender=transaction_notification, notification=notification)

    return HttpResponse("OK")


# Create your views here.
@require_POST
@csrf_exempt
def mbway_notification(request):
    log.info("mbway_notification, Easypay incoming POST data: \n%s", request.body)

    encoding = request.POST.get('charset', 'utf-8')
    data = QueryDict(request.body, encoding=encoding).copy()
    log.debug("Easypay MBWay notification data: %s", data)

    notification = MbwayNotification(data)
    log.debug("Easypay MBWay notification: %s", vars(notification))

    notification_received.send(sender=transaction_notification, notification=notification)

    return HttpResponse("OK")
