from django import forms
from .models import Ticket


class TicketSubmitForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["subject", "body", "submitted_by"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Describe your issue"}),
        }


class TicketCorrectionForm(forms.ModelForm):
    """Used by agents to fix/confirm category, urgency, status."""
    class Meta:
        model = Ticket
        fields = ["category", "urgency", "status", "assigned_agent"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "urgency": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "assigned_agent": forms.Select(attrs={"class": "form-select"}),
        }