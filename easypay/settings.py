from django.conf import settings


BACKEND_URL = getattr(settings, 'EASYPAY_BACKEND_URL', 'https://api.test.easypay.pt/2.0')
ACCOUNT_ID = getattr(settings, 'EASYPAY_ACCOUNT_ID', None)
API_KEY = getattr(settings, 'EASYPAY_API_KEY', None)

GENERATE_MERCHANT_KEY = getattr(settings, 'EASYPAY_GENERATE_MERCHANT_KEY', True)

PERSIST_TRANSACTIONS_CLASS = getattr(settings, 'EASYPAY_PERSIST_TRANSACTIONS_CLASS', None)  # app_label.model_name

NOTIFICATION_CODE_GENERIC = getattr(settings, 'EASYPAY_NOTIFICATION_CODE_GENERIC', None)
NOTIFICATION_CODE_AUTHORISATION = getattr(settings, 'EASYPAY_NOTIFICATION_CODE_AUTHORISATION', None)
NOTIFICATION_CODE_TRANSACTION = getattr(settings, 'EASYPAY_NOTIFICATION_CODE_TRANSACTION', None)
