import requests

endpoint = "http://localhost:8000/api/auth/register/"

token_obtain_pair = "http://localhost:8000/api/token/"
token_response = requests.post(token_obtain_pair,)


response = requests.post(endpoint, json={
    'name': 'anes',
    'password': 'testing321',
    'password_confirm': 'testing321',
    'phone_number': '0658025173',
    'user_type': 'assistant',
    'service_type': 'towing',
    'vehicle_type': 'towing truck',
    'location': {'longitude': 2342, 'latitude': 243},
    'driving_license_cat': 'b',
    'driving_license_num': 54543344,
    'driving_license_expiry': "20:08:2026"
})

print(response.json())
