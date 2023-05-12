from django.contrib import admin
from .models import *

class LogosAdmin(admin.ModelAdmin):
    list_display = ('image',)

class MustPayAdmin(admin.ModelAdmin):
    list_display = ('name_and_lastname', 'address', 'phone_number', 'job_status')

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name_and_lastname', 'address', 'phone_number')

class RecipientChildAdmin(admin.ModelAdmin):
    list_display =('name_and_lastname', 'recipient', 'birthday')

class MustPayReceiptAdmin(admin.ModelAdmin):
    list_display = ('must_pay', 'full_assessment', 'payment', 'payment_date', 'alimony_percent')

class AlimonyAdmin(admin.ModelAdmin):
    list_display =('executor_register','must_pay', 'recipient', 'began_paying', 'created_at', 'ruling', 'category', 'user', 'status')

admin.site.register(Logos, LogosAdmin)
admin.site.register(MustPay, MustPayAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(RecipientChild, RecipientChildAdmin)
admin.site.register(MustPayReceipt, MustPayReceiptAdmin)
admin.site.register(Alimony, AlimonyAdmin)