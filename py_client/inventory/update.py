import requests
from getpass import getpass

# Assuming the necessary endpoints and authentication are already defined
auth_endpoint = "http://localhost:8001/api/users/login/"
username = input("What is your username?\n")
password = getpass("What is your password?\n")

# Authenticate user
auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Get the initial data for the inventory item you want to update
    item_id = 1  # Replace with the actual item ID you want to update
    endpoint = f"http://localhost:8001/api/inventory-update/{item_id}/" 
    
    get_response = requests.get(endpoint, headers=headers)
    
    if get_response.status_code == 200:
        # Fetch the current price_per_unit
        current_data = get_response.json()
        initial_price = current_data.get('price_per_unit', None)

        # Prepare data for update
        data = {
            "category": 1,  # Change as needed
            "price_per_unit": initial_price,  # Use the fetched initial price
            "name": "Updated Paracetimols",
            "quantity": 10
        }
        
        # Make the PUT request to update the item
        update_response = requests.put(endpoint, json=data, headers=headers)
        print(update_response.status_code)

        if update_response.status_code == 200:
            # Handle successful update
            updated_data = update_response.json()

            print(updated_data)
        else:
            print("Error updating item:", update_response.json())
    else:
        print("Error fetching item:", get_response.json())
