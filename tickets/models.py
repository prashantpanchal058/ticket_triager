from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ("billing", "Billing"),
        ("account", "Account"),
        ("orders", "Orders"),
        ("shipping", "Shipping"),
        ("refund", "Refund"),
        ("technical", "Technical"),
        ("product", "Product"),
        ("subscription", "Subscription"),
    ]

    URGENCY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    subject = models.CharField(max_length=255)
    body = models.TextField()

    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True
    )
    urgency = models.CharField(
        max_length=10, choices=URGENCY_CHOICES, blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submitted_tickets"
    )
    assigned_agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets"
    )

    category_confidence = models.FloatField(null=True, blank=True)
    urgency_confidence = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.get_status_display()})"

    class Meta:
        ordering = ["-created_at"]