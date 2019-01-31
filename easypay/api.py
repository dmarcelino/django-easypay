from enum import Enum, unique
from numbers import Number
import json
import requests
from . import settings


AUTH_HEADERS = {
    'AccountId': settings.ACCOUNT_ID,
    'ApiKey': settings.API_KEY,
}


def get_messages(response_dict):
    """
    docs say 'messages' but server returns 'message'...
    :param response_dict:
    :return:
    """
    if 'messages' in response_dict:
        return response_dict.get('messages')
    else:
        return response_dict.get('message')


@unique
class Type(Enum):
    SALE = 'sale'
    AUTHORISATION = 'authorisation'


@unique
class MethodEnum(Enum):
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


class EasypayApiException(Exception):
    """Exception raised for Easypay API failed requests."""
    status = None
    messages = []
    response = None

    def __init__(self, response):
        try:
            response_dict = response.json()
            status = response_dict.get('status')
            messages = get_messages(response_dict)
        except: # noqa
            status = status or response.status_code
            messages = [response.text or ""]
        self.status = status
        self.messages = messages
        self.response = response
        message = 'Call to {uri} returned {status}, errors: \n - {errors}'.format(
            uri=response.url,
            status=status,
            errors='\n - '.join(messages)
        )

        super(EasypayApiException, self).__init__(message)


class PaymentMethod:
    def __init__(self, dict):
        """
        Initialise PaymentMethod
        :param dict: 'method' dict from Easypay response
        """
        self.method_type = MethodEnum(dict.get('type', '').lower())
        self.entity = dict.get('entity')
        self.reference = dict.get('reference')
        self.url = dict.get('url')
        self.last_four = dict.get('last_four')
        self.card_type = dict.get('card_type')
        self.expiration_date = dict.get('expiration_date')
        self.alias = dict.get('alias')
        self.status = dict.get('status')

    def __str__(self):
        return 'PaymentMethod reference: {}'.format(self.reference)


class Customer:
    def __init__(self, data):
        """
        Initialise Customer
        :param data: 'customer' dict from Easypay message
        """
        self.id = data.get('id')
        self.name = data.get('name')
        self.email = data.get('email')
        self.phone = data.get('phone')
        self.phone_indicative = data.get('phone_indicative')
        self.fiscal_number = data.get('fiscal_number')
        self.key = data.get('key')

    def __str__(self):
        return 'Customer id: {}'.format(self.id)


class Transaction:
    def __init__(self, data):
        """
        Initialise Transaction
        :param data: 'transaction' dict from Easypay message
        """
        self.id = data.get('id')
        self.key = data.get('key')
        self.transaction_type = data.get('type')
        self.date = data.get('date')
        self.values = data.get('values')
        self.transfer_date = data.get('transfer_date')
        self.document_number = data.get('document_number')

    def __str__(self):
        return 'Transaction id: {}'.format(self.id)


class PaymentResponse:
    def __init__(self, response):
        """
        Initialise PaymentResponse
        :param response: requests Response from Easypay
        """
        response_dict = response.json()
        self.status = response_dict.get('status')
        self.messages = get_messages(response_dict)
        self.id = response_dict.get('id')
        self.method = PaymentMethod(response_dict.get('method'))
        self.customer_id = response_dict.get('customer', {}).get('id')
        self.response = response

    def __str__(self):
        return 'PaymentResponse id: {}'.format(self.id)


class TransactionNotification:
    def __init__(self, request_dict):
        self.id = request_dict.get('id')
        self.value = request_dict.get('value')
        self.currency = request_dict.get('currency')
        self.merchant_key = request_dict.get('key')
        self.expiration_time = request_dict.get('expiration_time')
        self.customer = Customer(request_dict.get('customer', {}))
        self.method = request_dict.get('method')
        self.transaction = Transaction(request_dict.get('transaction', {}))
        self.account_id = request_dict.get('account', {}).get('id')
        self.request = request_dict

    def __str__(self):
        return 'TransactionNotification id: {}'.format(self.id)


def single_payment(value, payment_type=Type.SALE.value, method=MethodEnum.MULTIBANCO.value,
                   capture_transaction_key=None, capture_date=None, capture_descriptive=None, expiration_time=None,
                   currency='EUR', customer_account_id=None, customer_name=None, customer_email=None,
                   customer_phone=None, customer_phone_indicative='+351', customer_fiscal_number=None,
                   customer_key=None, merchant_key=None, user=None):
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
    :return:
    """
    check_auth_params()
    url = "{}/single".format(settings.BACKEND_URL)

    if not isinstance(value, Number):
        raise ValueError('value must be a number.')

    if not MethodEnum.has_value(method):
        raise ValueError('method must be one of {}.'.format(MethodEnum.list()))

    if not merchant_key and settings.MERCHANT_KEY:
        merchant_key = settings.MERCHANT_KEY

    if user:
        if not customer_name:
            customer_name = user.get_full_name()
        if not customer_email:
            customer_email = user.email
        if not customer_key:
            customer_key = str(user.id)

    payload = {
        'type': payment_type,
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

    if not r.ok:
        raise EasypayApiException(r)
    return PaymentResponse(r)


def get_payment(id):
    """
    Shows single payment details
    :param id: string <uuid> Required  Resource Identification
    :return:
    """
    check_auth_params()
    url = "{}/single/{}".format(settings.BACKEND_URL,id)

    if not id:
        raise ValueError('id must be a UUID string.')

    r = requests.get(url, headers=AUTH_HEADERS)

    if not r.ok:
        raise EasypayApiException(r)
    return PaymentResponse(r)


def delete_payment(id):
    """
    Deletes single payment
    :param id: string <uuid> Required  Resource Identification
    :return:
    """
    check_auth_params()
    url = "{}/single/{}".format(settings.BACKEND_URL,id)

    if not id:
        raise ValueError('id must be a UUID string.')

    r = requests.delete(url, headers=AUTH_HEADERS)
    return r


def check_auth_params():
    if not (settings.ACCOUNT_ID and isinstance(settings.ACCOUNT_ID, str)):
        raise ValueError('EASYPAY_ACCOUNT_ID setting is invalid.')
    if not (settings.API_KEY and isinstance(settings.API_KEY, str)):
        raise ValueError('API_KEY setting is invalid.')
