from django.contrib import admin
from apps.ticket_detail.models import TicketDetail

from django.contrib import admin
from .models import TicketDetail


class TicketDetailAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_id",
        "quantity",
        "is_menu",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("ticket_id__id", "description")
    list_filter = ("ticket_id", "status", "created_at", "updated_at")
    fields = ("ticket_id", "quantity", "is_menu", "description", "status")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(TicketDetail, TicketDetailAdmin)
