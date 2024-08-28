from django.contrib import admin
from .models import *
# Register your models here.
# @admin.ModelAdmin()

class TransactionInline(admin.StackedInline):
    model=owee
    extra=1

class ModalTransaction(admin.ModelAdmin):
    inlines=[TransactionInline]

    
admin.site.register(Transaction,ModalTransaction)
admin.site.register(Profile)