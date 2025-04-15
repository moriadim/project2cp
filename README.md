# Depannini Project - Backend & Frontend Integration Guide

## Backend Overview

The Depannini project uses Django with JWT authentication for the backend and Flutter for the frontend. This README provides instructions for setting up and integrating both components.

### Current Status

✅ Django backend with JWT authentication  
✅ User registration and authentication flows  
✅ Email and phone verification systems  
✅ User profile management  
✅ Access control for different user types (users, assistants, admins)  

## Getting Started with the Backend

### Prerequisites

- Python 3.9+
- pip
- virtualenv
- PostgreSQL (recommended) or SQLite

### Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd depannini
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost/depannini
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/verify-email/` - Email verification
- `POST /api/auth/verify-phone/` - Phone verification
- `POST /api/auth/login/email/` - Email login
- `POST /api/auth/login/phone/` - Phone login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/confirm/` - Confirm password reset

### User Profiles

- `GET /api/profile/user/` - Get user profile
- `PUT /api/profile/user/` - Update user profile
- `GET /api/profile/assistant/` - Get assistant profile
- `PUT /api/profile/assistant/` - Update assistant profile

## Remaining Backend Tasks

- [ ] Configure SMS service for phone verification
- [ ] Set up email service for production
- [ ] Implement location-based assistant matching
- [ ] Add rating system for assistants
- [ ] Create payment integration
- [ ] Configure production deployment settings
- [ ] Implement API rate limiting

## Flutter Frontend Integration

### Setting Up Flutter Project

1. Install Flutter SDK: [Flutter Installation Guide](https://flutter.dev/docs/get-started/install)

2. Create a new Flutter project:
```bash
flutter create depannini_app
cd depannini_app
```

3. Add required dependencies to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.5
  shared_preferences: ^2.0.15
  provider: ^6.0.3
  flutter_secure_storage: ^6.0.0
  jwt_decoder: ^2.0.1
  google_maps_flutter: ^2.2.0
  image_picker: ^0.8.6
  intl: ^0.17.0
```

4. Run `flutter pub get` to install dependencies

### Implementing API Services

1. Create an API client class:
```dart
// lib/services/api_client.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  final String baseUrl = 'http://10.0.2.2:8000/api';  // Use your own IP for physical devices
  final storage = FlutterSecureStorage();
  
  Future<Map<String, String>> _getHeaders({bool requiresAuth = true}) async {
    Map<String, String> headers = {
      'Content-Type': 'application/json',
    };
    
    if (requiresAuth) {
      final token = await storage.read(key: 'access_token');
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }
    
    return headers;
  }
  
  Future<dynamic> get(String endpoint, {bool requiresAuth = true}) async {
    final response = await http.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: await _getHeaders(requiresAuth: requiresAuth),
    );
    
    return _processResponse(response);
  }
  
  Future<dynamic> post(String endpoint, dynamic data, {bool requiresAuth = true}) async {
    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: await _getHeaders(requiresAuth: requiresAuth),
      body: jsonEncode(data),
    );
    
    return _processResponse(response);
  }
  
  Future<dynamic> put(String endpoint, dynamic data, {bool requiresAuth = true}) async {
    final response = await http.put(
      Uri.parse('$baseUrl$endpoint'),
      headers: await _getHeaders(requiresAuth: requiresAuth),
      body: jsonEncode(data),
    );
    
    return _processResponse(response);
  }
  
  dynamic _processResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to process request: ${response.body}');
    }
  }
}
```

2. Create authentication service:
```dart
// lib/services/auth_service.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'api_client.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();
  final FlutterSecureStorage _storage = FlutterSecureStorage();
  
  Future<Map<String, dynamic>> register(Map<String, dynamic> userData) async {
    final response = await _apiClient.post('/auth/register/', userData, requiresAuth: false);
    await _storeTokens(response);
    return response;
  }
  
  Future<Map<String, dynamic>> loginWithEmail(String email, String password) async {
    final response = await _apiClient.post(
      '/auth/login/email/',
      {'email': email, 'password': password},
      requiresAuth: false,
    );
    await _storeTokens(response);
    return response;
  }
  
  Future<void> _storeTokens(Map<String, dynamic> response) async {
    await _storage.write(key: 'access_token', value: response['access']);
    await _storage.write(key: 'refresh_token', value: response['refresh']);
  }
  
  Future<void> logout() async {
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
  }
  
  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }
  
  Future<Map<String, dynamic>> refreshToken() async {
    final refreshToken = await _storage.read(key: 'refresh_token');
    if (refreshToken == null) {
      throw Exception('No refresh token available');
    }
    
    final response = await _apiClient.post(
      '/auth/token/refresh/',
      {'refresh': refreshToken},
      requiresAuth: false,
    );
    
    await _storage.write(key: 'access_token', value: response['access']);
    return response;
  }
}
```

### Frontend Screens to Implement

1. Authentication Screens:
   - Login Screen
   - Registration Screen
   - Verification Screens (Email & Phone)
   - Password Reset Screen

2. User Profile Screens:
   - User Profile
   - Assistant Profile
   - Edit Profile

3. Core Functionality:
   - Home Screen with Map View
   - Assistant Search/Filter
   - Service Request Form
   - Request Status Tracking
   - Rating System

## Remaining Frontend Tasks

- [ ] Design wireframes and UI components
- [ ] Implement authentication flow
- [ ] Build user profile management
- [ ] Develop location services integration
- [ ] Create service request workflow
- [ ] Implement real-time notifications
- [ ] Add payment integration
- [ ] Develop ratings and reviews system
- [ ] Implement chat functionality

## Next Steps for Integration

1. **Complete Backend Configuration:**
   - Finalize SMS service integration
   - Configure email service for production
   - Set up environment variables and secrets management

2. **Test API Endpoints:**
   - Use Postman to verify all endpoints are working correctly   hadi say verifit
   - Document any API changes or additions

3. **Implement Frontend Components:**
   - Start with authentication screens
   - Build profile management screens
   - Create core service request functionality

4. **Connect Frontend with Backend:**
   - Ensure proper token handling
   - Implement error handling and network state management
   - Test the complete flow from registration to service requests

5. **Prepare for Deployment:**
   - Configure production settings for Django
   - Set up CI/CD pipeline
   - Prepare app for store submission

## Contact

For any questions or assistance with the integration, please contact the project team.

---

© 2025 Depannini Project
