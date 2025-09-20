from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import re
from django.core.exceptions import ValidationError

# ------------------ Validators ------------------

def validate_egyptian_phone(value):
    pattern = r"^(010|011|012|015)[0-9]{8}$"
    if not re.match(pattern, value):
        raise ValidationError("Invalid Egyptian phone number format.")

# ------------------ Custom User ------------------

class User(AbstractUser):
    username = None  
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True, validators=[validate_egyptian_phone])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

# ------------------ Project Model ------------------

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    details = models.TextField()
    total_target = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
