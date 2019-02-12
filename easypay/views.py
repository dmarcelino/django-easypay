from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

from . import settings, signals
from .api import GenericNotification, TransactionNotification, MbwayNotification, get_payment


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

    easypay_code = request.META.get('HTTP_X_EASYPAY_CODE')
    log.debug("generic_notification, Easypay X_EASYPAY_CODE header: \n%s", easypay_code)
    if settings.NOTIFICATION_CODE_GENERIC and settings.NOTIFICATION_CODE_GENERIC != easypay_code:
        log.warning("generic_notification, permission denied, X_EASYPAY_CODE: \n%s", easypay_code)
        raise PermissionDenied("Permission Denied")

    encoding = request.POST.get('charset', 'utf-8')
    data = json.loads(request.body.decode(encoding))

    notification = GenericNotification(data)

    log.debug("Easypay generic notification: %s", vars(notification))

    signals.generic_notification.send(sender=generic_notification, notification=notification)

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

    easypay_code = request.META.get('HTTP_X_EASYPAY_CODE')
    log.debug("generic_notification, Easypay X_EASYPAY_CODE header: \n%s", easypay_code)
    if settings.NOTIFICATION_CODE_AUTHORISATION and settings.NOTIFICATION_CODE_AUTHORISATION != easypay_code:
        log.warning("authorisation_notification, permission denied, X_EASYPAY_CODE: \n%s", easypay_code)
        raise PermissionDenied("Permission Denied")

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

    easypay_code = request.META.get('HTTP_X_EASYPAY_CODE')
    log.debug("generic_notification, Easypay X_EASYPAY_CODE header: \n%s", easypay_code)
    if settings.NOTIFICATION_CODE_TRANSACTION and settings.NOTIFICATION_CODE_TRANSACTION != easypay_code:
        log.warning("transaction_notification, permission denied, X_EASYPAY_CODE: \n%s", easypay_code)
        raise PermissionDenied("Permission Denied")

    encoding = request.POST.get('charset', 'utf-8')
    data = json.loads(request.body.decode(encoding))

    notification = TransactionNotification(data)

    log.debug("Easypay transaction notification: %s, transaction: %s",
              vars(notification), vars(notification.transaction))

    if settings.PERSIST_TRANSACTIONS_CLASS:
        try:
            PaymentModel = apps.get_model(settings.PERSIST_TRANSACTIONS_CLASS)
            payment_record = PaymentModel.objects.get(easypay_id=notification.transaction.id)
            payment_response = get_payment(notification.transaction.id)  # we could probably use the notification
            payment_record.update(payment_response)
            log.debug('Updated payment with id [%s] in the database.', notification.transaction.id)
        except Exception as e:
            log.error('Failed to update payment with id [%s] in the database, error: %s.', notification.transaction.id, e, exc_info=True)

    signals.transaction_notification.send(sender=transaction_notification, notification=notification)

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

    signals.mbway_notification.send(sender=mbway_notification, notification=notification)

    return HttpResponse("OK")
