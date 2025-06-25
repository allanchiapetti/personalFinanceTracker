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
