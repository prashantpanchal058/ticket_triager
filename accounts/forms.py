from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Choose a username",
            "email": "you@example.com",
            "password1": "Create a password",
            "password2": "Repeat your password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": placeholders.get(name, ""),
            })

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data["email"] 
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError( "This email is already registered." ) 
        return email