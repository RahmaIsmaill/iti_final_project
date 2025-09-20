from django import forms
from .models import User, Project
from django.core.exceptions import ValidationError
from datetime import date
import re

# ------------------ User Forms ------------------

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
        required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            raise ValidationError("Phone number is required.")
        pattern = r"^(010|011|012|015)[0-9]{8}$"
        if not re.match(pattern, phone):
            raise ValidationError("Invalid Egyptian phone number format (e.g., 010xxxxxxxx).")
        return phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("First name is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("Last name is required.")
        return last_name

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise ValidationError("Password is required.")
        return password

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pw and cpw and pw != cpw:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

# ------------------ Login Form ------------------

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")

# ------------------ Project Form ------------------

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # Must match model fields exactly
        fields = ['title', 'details', 'total_target', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

    def clean_total_target(self):
        amount = self.cleaned_data.get("total_target")
        if amount is None or amount <= 0:
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

