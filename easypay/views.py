from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

from .api import GenericNotification, TransactionNotification, MbwayNotification
from .signals import notification_received


log = logging.getLogger(__name__)


# Create your views here.
@require_POST
@csrf_exempt
def generic_notification(request):
    """
    Generic Notification endpoint
    :param request:
    :return:
    """
    log.info("generic_notification, Easypay incoming POST data: \n%s", request.body)
    log.debug("generic_notification, Easypay headers: \n%s", request.META)

    encoding = request.POST.get('charset', 'utf-8')
    data = json.loads(request.body.decode(encoding))

    notification = GenericNotification(data)

    log.debug("Easypay generic notification: %s", vars(notification))

    notification_received.send(sender=generic_notification, notification=notification)

    return HttpResponse("OK")


@require_POST
@csrf_exempt
def authorisation_notification(request):
    """
    Authorisation Notification endpoint
    :param request:
    :return:
    """
    log.info("authorisation_notification, Easypay incoming POST data: \n%s", request.body)
    log.debug("authorisation_notification, Easypay headers: \n%s", request.META)
    raise NotImplementedError('authorisation_notification not implemented')


@require_POST
@csrf_exempt
def transaction_notification(request):
    """
    Transaction Notification endpoint
    :param request:
    :return:
    """
    log.info("transaction_notification, Easypay incoming POST data: \n%s", request.body)
    log.debug("transaction_notification, Easypay headers: \n%s", request.META)

    encoding = request.POST.get('charset', 'utf-8')
    data = json.loads(request.body.decode(encoding))

    notification = TransactionNotification(data)

    log.debug("Easypay transaction notification: %s", vars(notification))

    notification_received.send(sender=transaction_notification, notification=notification)

    return HttpResponse("OK")


# Create your views here.
@require_POST
@csrf_exempt
def mbway_notification(request):
    log.info("mbway_notification, Easypay incoming POST data: \n%s", request.body)

    encoding = request.POST.get('charset', 'utf-8')
    data = QueryDict(request.body, encoding=encoding).copy()

    notification = MbwayNotification(data)
    log.debug("Easypay MBWay notification: %s", vars(notification))

    notification_received.send(sender=transaction_notification, notification=notification)

    return HttpResponse("OK")
