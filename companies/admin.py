from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "ticker", "docname", "docid", "orgid", "tablename", "currency", "particulars", "amount")
    search_fields = ("ticker", "docname", "docid", "orgid", "particulars")
    list_filter = ("currency", "tablename")
    ordering = ("ticker",)