from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "category", "urgency", "status", "created_at")
    list_filter = ("category", "urgency", "status")
    search_fields = ("subject", "body", "submitted_by")
    

    def category_display(self, obj):
        if obj.category_confidence is not None:
            return f"{obj.get_category_display()} ({obj.category_confidence * 100:.0f}%)"
        return obj.get_category_display() or "—"
    category_display.short_description = "Category"

    def urgency_display(self, obj):
        if obj.urgency_confidence is not None:
            return f"{obj.get_urgency_display()} ({obj.urgency_confidence * 100:.0f}%)"
        return obj.get_urgency_display() or "—"
    urgency_display.short_description = "Urgency"