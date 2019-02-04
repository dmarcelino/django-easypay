from django.contrib import admin


# Register your models here.
class EasypayPaymentAdmin(admin.ModelAdmin):
    list_display = ('easypay_id', 'merchant_key', 'amount', 'status', 'method_type', 'customer_id', 'customer_id',
                    'user', 'created_at', 'updated_at')
