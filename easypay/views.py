from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

from .api import TransactionNotification
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
    log.warning("Easypay incoming POST data: %s", request.body)  # TODO: info

    encoding = request.POST.get('charset', 'utf-8')
    data = json.loads(request.body.decode(encoding))

    notification = TransactionNotification(data)

    log.debug("Easypay notification: %s", notification)

    notification_received.send(sender=transaction_notification, notification=notification)

    return HttpResponse("OK")
