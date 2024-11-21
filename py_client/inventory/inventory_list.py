import requests
from getpass import getpass

auth_endpoint = "http://localhost:8001/api/users/login/" 
username = input("What is your username?\n")
password = getpass("What is your password?\n")

auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password}) 
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://localhost:8001/api/inventory-list/" 

    get_response = requests.get(endpoint, headers=headers) 
    print(get_response.status_code)
    data = get_response.json()
    for item in data:
        print(f"ID: {item['id']}, Name: {item['name']}, Quantity: {item['quantity']}")