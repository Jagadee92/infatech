from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "ticker", "industry", "current_price", "market_cap")
    search_fields = ("name", "ticker", "industry")
