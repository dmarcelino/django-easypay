from django.conf import settings


BACKEND_URL = getattr(settings, 'EASYPAY_BACKEND_URL', 'https://api.test.easypay.pt/2.0')
ACCOUNT_ID = getattr(settings, 'EASYPAY_ACCOUNT_ID', None)
API_KEY = getattr(settings, 'EASYPAY_API_KEY', None)

MERCHANT_KEY = getattr(settings, 'EASYPAY_MERCHANT_KEY', None)
