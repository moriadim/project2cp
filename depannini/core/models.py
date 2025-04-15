# core/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('user', 'Regular User'),
        ('assistant', 'Assistant'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('depanneur', 'Depanneur'),
        ('reparateur', 'Reparateur'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    location = models.JSONField(blank=True, null=True)  # Storing lat/long as JSON
    address = models.CharField(max_length=255, blank=True, null=True)
    
    # Fields for assistants
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES, blank=True, null=True)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    is_active_assistant = models.BooleanField(default=False)
    
    # Standard Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    @property
    def is_assistant(self):
        return self.user_type == 'assistant'


class VerificationCode(models.Model):
    CODE_TYPE_CHOICES = [
        ('email', 'Email Verification'),
        ('phone', 'Phone Verification'),
        ('password', 'Password Reset'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=10)
    code_type = models.CharField(max_length=10, choices=CODE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code_type} code for {self.user.email}"

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()