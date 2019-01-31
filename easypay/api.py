from enum import Enum
from numbers import Number
import json
import requests
from . import settings


AUTH_HEADERS = {
    'AccountId': settings.ACCOUNT_ID,
    'ApiKey': settings.API_KEY,
}


class Type(Enum):
    SALE = 'sale'
    AUTHORISATION = 'authorisation'


class Method(Enum):
    MULTIBANCO = 'mb'
    CC = 'cc'
    BB = 'bb'
    MBWAY = 'mbw'
    DEBITO_DIRECTO = 'dd'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


def authentication():
    check_auth_params()
    url = "{}/single".format(settings.BACKEND_URL)
    payload = {
        'type': Type.AUTHORISATION.value,
        'value': 1.0,
        'method': Method.MULTIBANCO.value,
    }
    r = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(payload))
    return r


def single_payment(value, method=Method.MULTIBANCO.value, capture_transaction_key=None, capture_date=None,
                   capture_descriptive=None, expiration_time=None, currency='EUR', customer_account_id=None,
                   customer_name=None, customer_email=None, customer_phone=None, customer_phone_indicative='+351',
                   customer_fiscal_number=None, customer_key=None, merchant_key=None, user=None):
    """
    Payments used on a one time purchase

    :param value: number <double> Required
    :param method: string Required valid values "mb" "cc" "bb" "mbw" "dd"
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
    :return:
    """
    check_auth_params()
    url = "{}/single".format(settings.BACKEND_URL)

    if not isinstance(value, Number):
        raise ValueError('value must be a number.')

    if not Method.has_value(method):
        raise ValueError('method must be one of {}.'.format(Method.list()))

    if user:
        if not customer_name:
            customer_name = user.get_full_name()
        if not customer_email:
            customer_email = user.email
        if not customer_key:
            customer_key = str(user.id)

    payload = {
        'type': Type.SALE.value,
        'capture': {
            'transaction_key': capture_transaction_key,
            'capture_date': capture_date,
            'account': {
                'id': customer_account_id,
            },
            'descriptive': capture_descriptive,
        },
        'expiration_time': expiration_time,
        'currency': currency,
        'customer': {
            'id': customer_account_id,
            'name': customer_name,
            'email': customer_email,
            'phone': customer_phone,
            'phone_indicative': customer_phone_indicative,
            'fiscal_number': customer_fiscal_number,
            'key': customer_key,
        },
        'key': merchant_key,
        'value': value,
        'method': method,
    }
    r = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(payload))
    return r


def get_payment(id):
    check_auth_params()
    url = "{}/single/{}".format(settings.BACKEND_URL,id)

    if not id:
        raise ValueError('id must be a UUID string.')

    r = requests.get(url, headers=AUTH_HEADERS)
    return r


def check_auth_params():
    if not (settings.ACCOUNT_ID and isinstance(settings.ACCOUNT_ID, str)):
        raise ValueError('EASYPAY_ACCOUNT_ID setting is invalid.')
    if not (settings.API_KEY and isinstance(settings.API_KEY, str)):
        raise ValueError('API_KEY setting is invalid.')
