# core/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(phone_number=phone_number, **extra_fields)
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
        ('client', 'Client'),
        ('assistant', 'Assistant'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('towing', 'Towing'),
        ('repair', 'Repair'),
    ]

    License_Category_CHOICES = [
        ('c', 'C'),
        ('b', 'B'),
    ]

    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(
        max_length=20, blank=False, null=False, unique=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/', blank=True, null=True)
    # Storing lat/long as JSON
    location = models.JSONField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)

    # Fields for assistants
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default='client')
    service_type = models.CharField(
        max_length=10, choices=SERVICE_TYPE_CHOICES, blank=True, null=True)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    is_active_assistant = models.BooleanField(default=False)

    driving_license_cat = models.CharField(
        max_length=1, choices=License_Category_CHOICES, null=True, blank=True)
    driving_license_num = models.CharField(
        max_length=12, null=True, blank=True)
    driving_license_expiry = models.DateField(null=True, blank=True)
    vehicle_registration_num = models.IntegerField(null=True, blank=True)

    # Standard Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        if self.email is not None:
            return self.email
        return self.name

    @property
    def is_assistant(self):
        return self.user_type == 'assistant'


class VerificationCode(models.Model):
    CODE_TYPE_CHOICES = [
        ('email', 'Email Verification'),
        ('phone', 'Phone Verification'),
        ('password', 'Password Reset'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=10)
    code_type = models.CharField(max_length=10, choices=CODE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code_type} code for {self.user.email}"

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()


class Assistance(models.Model):
    ASSISTANCE_STATUE_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    ASSISTANCE_STATUE_TYPE = [
        ('repair', 'Repair'),
        ('towing', 'Towing'),
    ]

    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assistances_as_client")
    assistant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assistances_as_assistant", null=True, blank=True)

    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_lng = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    status = models.CharField(max_length=10, choices=ASSISTANCE_STATUE_CHOICES)
    rating = models.SmallIntegerField(default=0)

    distance_km = models.FloatField(default=0.0)
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.0)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Assistance #{self.id} - {self.status}"
