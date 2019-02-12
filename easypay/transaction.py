from django.apps import apps
import logging
from uuid import uuid4

from . import settings
from .api import single_payment as api_single_payment

log = logging.getLogger(__name__)


def _single_payment(*args, **kwargs):
    value = args[0]
    user = kwargs.pop('user', None)
    customer_name = kwargs.pop('customer_name', None)
    customer_email = kwargs.pop('customer_email', None)
    customer_key = kwargs.pop('customer_key', None)
    merchant_key = kwargs.pop('merchant_key', None)

    if not merchant_key and settings.GENERATE_MERCHANT_KEY:
        merchant_key = str(uuid4())

    if user:
        if not customer_name:
            customer_name = user.get_full_name()
        if not customer_email:
            customer_email = user.email
        if not customer_key:
            customer_key = str(user.id)

    log.debug('Making easypay payment request with args: '
              'merchant_key=%s, customer_name=%s, customer_email=%s, customer_key=%s, args: %s, kwargs: %s',
              merchant_key, customer_name, customer_email, customer_key, args, kwargs)

    payment_response = api_single_payment(merchant_key=merchant_key, customer_name=customer_name,
                                          customer_email=customer_email, customer_key=customer_key, *args, **kwargs)

    payment_record = None
    if settings.PERSIST_TRANSACTIONS_CLASS:
        try:
            PaymentModel = apps.get_model(settings.PERSIST_TRANSACTIONS_CLASS)
            payment_record = PaymentModel.create(merchant_key, value, payment_response, user)
            payment_record.save()
        except Exception as e:
            log.error('Failed to save payment with id [%s] to database, error: %s.', payment_response.id, e, exc_info=True)

    return payment_response, payment_record


def single_payment(*args, **kwargs):
    """
    Payments used on a one time purchase

    :param value: number <double> Required
    :param payment_type: string valid values: "sale" "authorisation"
    :param method: string Required valid values: "mb" "cc" "bb" "mbw" "dd"
    :param capture_transaction_key: string Your internal key identifying this capture
    :param capture_date: string <YYYY-mm-dd>
    :param capture_descriptive: string This will appear in the bank statement/mbway application
    :param expiration_time: string <YYYY-mm-dd HH:MM> Optional - used only for expirable methods (mbw, cc , dd)
    :param currency: string Default: "EUR" Valid values: "EUR" "BRL"
    :param customer_account_id:  string <uuid> Optional - uuid from previous created customers
    :param customer_name: string
    :param customer_email: string
    :param customer_phone: string
    :param customer_phone_indicative: string Default: "+351"
    :param customer_fiscal_number: string Fiscal Number must be prefixed with country code
    :param customer_key: string
    :param merchant_key: string Merchant identification key
    :param user: Django User object optional
    :return: PaymentResponse
    """
    return _single_payment(*args, **kwargs)[0]


def single_payment_db(*args, **kwargs):
    """
    Payments used on a one time purchase. Same as single_payment but returns DB record as well

    :param value: number <double> Required
    :param payment_type: string valid values: "sale" "authorisation"
    :param method: string Required valid values: "mb" "cc" "bb" "mbw" "dd"
    :param capture_transaction_key: string Your internal key identifying this capture
    :param capture_date: string <YYYY-mm-dd>
    :param capture_descriptive: string This will appear in the bank statement/mbway application
    :param expiration_time: string <YYYY-mm-dd HH:MM> Optional - used only for expirable methods (mbw, cc , dd)
    :param currency: string Default: "EUR" Valid values: "EUR" "BRL"
    :param customer_account_id:  string <uuid> Optional - uuid from previous created customers
    :param customer_name: string
    :param customer_email: string
    :param customer_phone: string
    :param customer_phone_indicative: string Default: "+351"
    :param customer_fiscal_number: string Fiscal Number must be prefixed with country code
    :param customer_key: string
    :param merchant_key: string Merchant identification key
    :param user: Django User object optional
    :return: Tuple of PaymentResponse and Payment record
    """
    return _single_payment(*args, **kwargs)
