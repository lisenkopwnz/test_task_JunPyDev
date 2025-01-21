from django.contrib import admin

from finance.models import Revenue


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    pass
