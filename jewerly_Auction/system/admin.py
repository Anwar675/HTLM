from django.contrib import admin

from .models import ValuationRequest

@admin.register(ValuationRequest)
class ValuationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'carat_weight', 'grade', 'price_range')
    search_fields = ('name', 'phone', 'origin')
    list_filter = ('date', 'origin', 'color', 'clarity')
