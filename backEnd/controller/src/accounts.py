import os
import requests

MODEL_API_ENDPOINT = os.getenv("MODEL_API_ENDPOINT")

def get_user_accounts(user_id):
    # Call the user data endpoint from Model to retrieve the user accounts
    user_accounts = requests.get(url=f"{MODEL_API_ENDPOINT}/user/account", json={"user_id": user_id})

    # Check if the request was successful
    if user_accounts.status_code != 200:
        return None
    else:
        return user_accounts.json()
    
def update_account(update_json):
    update = requests.put(url=f"{MODEL_API_ENDPOINT}/user/account", json=update_json)

    return update.status_code == 200

def delete_account(delete_json):
    update = requests.delete(url=f"{MODEL_API_ENDPOINT}/user/account", json=delete_json)

    return update.status_code == 200

def create_account(create_json, user_id):
    # Add the user_id to the create_json to ensure the account is linked to the correct user
    create_json['user_id'] = user_id

    create = requests.post(url=f"{MODEL_API_ENDPOINT}/user/account", json=create_json)

    return create.status_code == 200