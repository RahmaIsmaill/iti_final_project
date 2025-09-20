from django import forms
from .models import User, Project
from django.core.exceptions import ValidationError
from datetime import date
import re

# ------------------ User Forms ------------------

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = r"^(010|011|012|015)[0-9]{8}$"
        if not re.match(pattern, phone):
            raise ValidationError("Invalid Egyptian phone number format.")
        return phone

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pw and cpw and pw != cpw:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

# ------------------ Login Form ------------------

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# ------------------ Project Form ------------------

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

    def clean_total_target(self):
        amount = self.cleaned_data.get("total_target")
        if amount <= 0:
            raise ValidationError("Total target must be positive.")
        return amount

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        if start and end:
            if start >= end:
                raise ValidationError("Start date must be before end date.")
            if start < date.today():
                self.add_error("start_date", "Start date cannot be in the past.")
        return cleaned
