import requests
from getpass import getpass


endpoint = "http://localhost:8000/api/api/token/"
phone_number = input("phone_number : ")
password = getpass("Password : ")
print(password)
auth_response = requests.post(
    endpoint, json={"phone_number": phone_number, "password": password})

print(auth_response.json())


# print(get_response.headers)
