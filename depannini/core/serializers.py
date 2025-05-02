# core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Assistance
from datetime import date

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'name', 'phone_number',
            'profile_photo', 'location',
            'address'
        ]


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'name', 'phone_number', 'profile_photo', 'location',
            'address', 'service_type', 'vehicle_type',
        ]


class AssistantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'name', 'phone_number', 'profile_photo', 'location',
            'address', 'service_type', 'vehicle_type', 'is_active_assistant',
            'driving_license_cat', 'driving_license_num', 'driving_license_expiry',
            'vehicle_registration_num',
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    driving_license_expiry = serializers.DateField(
        input_formats="%d:%m:%y at %H:%M",
        format="%d:%m:%y at %H:%M",
        required=False
    )

    class Meta:
        model = User
        fields = [
            'phone_number', 'email', 'name',
            'password', 'password_confirm',
            'user_type', 'service_type', 'vehicle_type',
            'driving_license_cat', 'driving_license_num', 'driving_license_expiry',
            'vehicle_registration_num', 'location', 'address'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if attrs.get('user_type') == 'assistant':
            if not attrs.get('service_type'):
                raise serializers.ValidationError(
                    {"service_type": "Service type is required for assistants"})
            if not attrs.get('vehicle_type'):
                raise serializers.ValidationError(
                    {"vehicle_type": "Vehicle type is required for assistants"})
            if not attrs.get('location'):
                raise serializers.ValidationError(
                    {"location": "Location is required for assistants"})
            if not attrs.get('driving_license_cat'):
                raise serializers.ValidationError(
                    {"driving_license_cat": "driving license category type is required for assistants"})
            if not attrs.get('driving_license_num'):
                raise serializers.ValidationError(
                    {"driving_license_num": "driving license number type is required for assistants"})
            if not attrs.get('driving_license_expiry'):
                raise serializers.ValidationError(
                    {"driving_license_expiry": "driving license expiry date type is required for assistants"})
            if attrs.get('driving_license_expiry') < date.today():
                raise serializers.ValidationError(
                    "Expiry date cannot be in the past.")
            if not attrs.get('vehicle_registration_num'):
                raise serializers.ValidationError(
                    {"vehicle_registration_num": "vehicle registration number type is required for assistants"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=5)


class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=5)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=5)
    new_password = serializers.CharField(
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."})
        return attrs


# class PhoneLoginSerializer(serializers.Serializer):
#   phone_number = serializers.CharField()
#   code = serializers.CharField(max_length=5)


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class PhoneLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField()


class UpdateLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class UserAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number']


class AssistanceSerializer(serializers.ModelSerializer):
    client = UserAssistanceSerializer(read_only=True)
    assistant = UserAssistanceSerializer(read_only=True, required=False)
    pickupLocation = serializers.SerializerMethodField()
    dropoffLocation = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(
        source='created_at', read_only=True, format="%d:%m:%y at %H:%M")
    updatedAt = serializers.DateTimeField(
        source='updated_at', read_only=True, format="%d:%m:%y at %H:%M")

    class Meta:
        model = Assistance
        fields = [
            'id', 'status', 'client', 'assistant',
            'pickupLocation', 'dropoffLocation',
            'distance_km', 'total_price',
            'createdAt', 'updatedAt'
        ]

    def get_pickupLocation(self, obj):
        return {'lat': obj.pickup_lat, 'lng': obj.pickup_lng}

    def get_dropoffLocation(self, obj):
        if obj.dropoff_lat and obj.dropoff_lng:
            return {'lat': obj.dropoff_lat, 'lng': obj.dropoff_lng}
        return None


class AssistanceRequestSerializer(serializers.Serializer):
    pickup = serializers.DictField(child=serializers.FloatField())
    dropoff = serializers.DictField(
        child=serializers.FloatField(), required=False)


class LocationUpdateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
