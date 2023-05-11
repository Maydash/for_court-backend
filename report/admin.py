from django.contrib import admin
from .models import *

class LogosAdmin(admin.ModelAdmin):
    list_display = ('image',)

class MustPayAdmin(admin.ModelAdmin):
    list_display = ('name_and_lastname', 'address', 'phone_number')

admin.site.register(Logos, LogosAdmin)
admin.site.register(MustPay, MustPayAdmin)