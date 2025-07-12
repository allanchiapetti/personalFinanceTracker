import os
import requests

MODEL_API_ENDPOINT = os.getenv("MODEL_API_ENDPOINT")

def get_user_accounts(user_id):
    """
    Retrieve the accounts associated with a given user ID by making a GET request to the Model API.
    Args:
        user_id (str or int): The unique identifier of the user whose accounts are to be retrieved.
    Returns:
        dict or None: A dictionary containing the user's account information if the request is successful,
        otherwise None.
    """
    # Call the user data endpoint from Model to retrieve the user accounts
    user_accounts = requests.get(url=f"{MODEL_API_ENDPOINT}/user/account", json={"user_id": user_id})

    # Check if the request was successful
    if user_accounts.status_code != 200:
        return None
    else:
        return user_accounts.json()
    
def update_account(update_json) -> bool:
    """
    Updates a user account by sending a PUT request to the model API endpoint with the provided JSON data.
    Args:
        update_json (dict): A dictionary containing the account information to update.
    Returns:
        bool: True if the update was successful (HTTP status code 200), False otherwise.
    """
    update = requests.put(url=f"{MODEL_API_ENDPOINT}/user/account", json=update_json)

    return update.status_code == 200

def delete_account(delete_json) -> bool:
    """
    Deletes a user account by sending a DELETE request to the model API.
    Args:
        delete_json (dict): A dictionary containing the necessary data to identify and delete the account.
    Returns:
        bool: True if the account was successfully deleted (HTTP 200), False otherwise.
    """
    update = requests.delete(url=f"{MODEL_API_ENDPOINT}/user/account", json=delete_json)

    return update.status_code == 200

def create_account(create_json, user_id) -> bool:
    """
    Creates a new account for a user by sending a POST request to the model API.
    Args:
        create_json (dict): The JSON payload containing account details to be created.
        user_id (int or str): The unique identifier of the user to whom the account will be linked.
    Returns:
        bool: True if the account was successfully created (HTTP 200), False otherwise.
    """
    # Add the user_id to the create_json to ensure the account is linked to the correct user
    create_json['user_id'] = user_id

    create = requests.post(url=f"{MODEL_API_ENDPOINT}/user/account", json=create_json)

    return create.status_code == 201