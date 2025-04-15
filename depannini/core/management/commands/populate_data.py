# core/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample users
        self.stdout.write('Creating sample users...')
        
        # Regular users
        regular_users = [
            {
                'email': 'user1@example.com',
                'name': 'Regular User 1',
                'password': 'password123',
                'user_type': 'user',
                'phone_number': '+1234567890',
                'email_verified': True,
                'phone_verified': True
            },
            {
                'email': 'user2@example.com',
                'name': 'Regular User 2',
                'password': 'password123',
                'user_type': 'user',
                'phone_number': '+1234567891',
                'email_verified': True,
                'phone_verified': True
            }
        ]
        
        for user_data in regular_users:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(
                    email=user_data['email'],
                    name=user_data['name'],
                    password=user_data['password'],
                    user_type=user_data['user_type'],
                    phone_number=user_data['phone_number']
                )
                user.email_verified = user_data['email_verified']
                user.phone_verified = user_data['phone_verified']
                user.save()
                self.stdout.write(f"Created user: {user.email}")
            else:
                self.stdout.write(f"User already exists: {user_data['email']}")
        
        # Assistant users
        locations = [
            {'latitude': 35.12345, 'longitude': -80.98765},
            {'latitude': 35.22345, 'longitude': -80.88765},
            {'latitude': 35.32345, 'longitude': -80.78765},
            {'latitude': 35.42345, 'longitude': -80.68765}
        ]
        
        service_types = ['depanneur', 'reparateur']
        vehicle_types = ['Tow Truck', 'Flatbed Truck', 'Service Van', 'Motorcycle']
        
        assistant_users = [
            {
                'email': 'assistant1@example.com',
                'name': 'Assistant User 1',
                'password': 'password123',
                'user_type': 'assistant',
                'phone_number': '+2234567890',
                'email_verified': True,
                'phone_verified': True,
                'service_type': service_types[0],
                'vehicle_type': vehicle_types[0],
                'location': locations[0],
                'is_active_assistant': True
            },
            {
                'email': 'assistant2@example.com',
                'name': 'Assistant User 2',
                'password': 'password123',
                'user_type': 'assistant',
                'phone_number': '+2234567891',
                'email_verified': True,
                'phone_verified': True,
                'service_type': service_types[1],
                'vehicle_type': vehicle_types[1],
                'location': locations[1],
                'is_active_assistant': True
            },
            {
                'email': 'assistant3@example.com',
                'name': 'Assistant User 3',
                'password': 'password123',
                'user_type': 'assistant',
                'phone_number': '+2234567892',
                'email_verified': True,
                'phone_verified': True,
                'service_type': service_types[0],
                'vehicle_type': vehicle_types[2],
                'location': locations[2],
                'is_active_assistant': False
            }
        ]
        
        for user_data in assistant_users:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(
                    email=user_data['email'],
                    name=user_data['name'],
                    password=user_data['password'],
                    user_type=user_data['user_type'],
                    phone_number=user_data['phone_number'],
                    service_type=user_data['service_type'],
                    vehicle_type=user_data['vehicle_type'],
                    location=user_data['location'],
                    is_active_assistant=user_data['is_active_assistant']
                )
                user.email_verified = user_data['email_verified']
                user.phone_verified = user_data['phone_verified']
                user.save()
                self.stdout.write(f"Created assistant: {user.email}")
            else:
                self.stdout.write(f"Assistant already exists: {user_data['email']}")
        
        self.stdout.write(self.style.SUCCESS('Sample data population complete!'))