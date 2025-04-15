# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .models import User, VerificationCode


class UserCreationForm(forms.ModelForm):
    """Form for creating new users in admin panel"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form for updating users in admin panel"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'phone_number', 'is_active', 'is_staff', 'user_type',
                  'service_type', 'vehicle_type', 'is_active_assistant', 'email_verified', 'phone_verified')

    def clean_password(self):
        # Return the initial value regardless of what the user provides
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    """Configure the admin interface for User model"""
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name', 'phone_number', 'user_type', 'is_staff', 'email_verified', 'phone_verified')
    list_filter = ('is_staff', 'user_type', 'email_verified', 'phone_verified')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number', 'profile_photo', 'location', 'address')}),
        ('Assistant info', {'fields': ('user_type', 'service_type', 'vehicle_type', 'is_active_assistant')}),
        ('Verification status', {'fields': ('email_verified', 'phone_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password1', 'password2', 'user_type'),
        }),
    )
    
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class VerificationCodeAdmin(admin.ModelAdmin):
    """Configure the admin interface for VerificationCode model"""
    list_display = ('user', 'code', 'code_type', 'created_at', 'expires_at', 'is_used')
    list_filter = ('code_type', 'is_used')
    search_fields = ('user__email', 'user__name', 'code')


# Register the models with admin site
admin.site.register(User, UserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)