# core/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, VerificationCode
from django.utils import timezone
from datetime import timedelta


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_email_url = reverse('login-email')
        self.verify_email_url = reverse('verify-email')
        
        # Create test user
        self.test_user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='password123'
        )
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'password123',
            'password_confirm': 'password123',
            'user_type': 'user'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        
        # Check user created in database
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
        # Check verification code created
        self.assertTrue(VerificationCode.objects.filter(
            user__email='newuser@example.com', 
            code_type='email'
        ).exists())
    
    def test_email_login(self):
        """Test email login"""
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = self.client.post(self.login_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
    
    def test_email_verification(self):
        """Test email verification"""
        # Create verification code
        code = 'ABC12'
        verification = VerificationCode.objects.create(
            user=self.test_user,
            code=code,
            code_type='email',
            expires_at=timezone.now() + timedelta(minutes=30)
        )
        
        # Authenticate user first
        self.client.force_authenticate(user=self.test_user)
        
        data = {
            'email': 'test@example.com',
            'code': code
        }
        
        response = self.client.post(self.verify_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check user's email_verified status
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.email_verified)
        
        # Check verification code marked as used
        verification.refresh_from_db()
        self.assertTrue(verification.is_used)


class AssistantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create assistant user
        self.assistant = User.objects.create_user(
            email='assistant@example.com',
            name='Test Assistant',
            password='password123',
            user_type='assistant',
            service_type='depanneur',
            vehicle_type='Tow Truck',
            location={'latitude': 35.12345, 'longitude': -80.98765},
            is_active_assistant=True
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            name='Test User',
            password='password123',
            user_type='user'
        )
        
        self.assistant_list_url = reverse('assistant-list')
        self.assistant_status_url = reverse('assistant-status')
    
    def test_assistant_list(self):
        """Test listing assistants"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.assistant_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], self.assistant.email)
    
    def test_assistant_status_toggle(self):
        """Test toggling assistant status"""
        self.client.force_authenticate(user=self.assistant)
        
        # Toggle to inactive
        data = {'is_active': False}
        response = self.client.post(self.assistant_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check status updated
        self.assistant.refresh_from_db()
        self.assertFalse(self.assistant.is_active_assistant)
        
        # Toggle back to active
        data = {'is_active': True}
        response = self.client.post(self.assistant_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check status updated
        self.assistant.refresh_from_db()
        self.assertTrue(self.assistant.is_active_assistant)
    
    def test_non_assistant_cannot_toggle_status(self):
        """Test that non-assistants cannot toggle status"""
        self.client.force_authenticate(user=self.user)
        
        data = {'is_active': True}
        response = self.client.post(self.assistant_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)