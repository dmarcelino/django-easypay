import json
import requests
from . import settings


AUTH_HEADERS = {
    'AccountId': settings.ACCOUNT_ID,
    'ApiKey': settings.API_KEY,
}


class PaymentType:
    SALE = 'sale'
    AUTHORISATION = 'authorisation'


class PaymentMethod:
    MULTIBANCO = 'mb'
    CC = 'cc'
    BB = 'bb'
    MBWAY = 'mbw'
    DEBITO_DIRECTO = 'dd'


def authentication():
    url = "{}/single".format(settings.BACKEND_URL)
    payload = {
        'type': PaymentType.AUTHORISATION,
        'value': 1.0,
        'method': PaymentMethod.MULTIBANCO,
    }
    r = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(payload))
    return r
