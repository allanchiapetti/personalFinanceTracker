import os
import requests

MODEL_API_ENDPOINT = os.getenv("MODEL_API_ENDPOINT")

def get_pending_transactions(user_id):
    """
    Retrieve the list of pending (unpaid) transactions for a given user.
    Args:
        user_id (str or int): The unique identifier of the user whose pending transactions are to be retrieved.
    Returns:
        list or dict or None: The JSON response containing the list of pending transactions if the request is successful,
        otherwise None.
    """
    # Call the user data endpoint from Model to retrieve the user pending transactions
    pending_transactions = requests.get(url=f"{MODEL_API_ENDPOINT}/user/transaction/unpaid", json={"user_id": user_id})

    # Check if the request was successful
    if pending_transactions.status_code != 200:
        return None
    else:
        return pending_transactions.json()

def get_spending_by_month(user_id):
    """
    Retrieves the user's monthly spending statistics by making a request to the Model API.
    Args:
        user_id (str or int): The unique identifier of the user whose spending data is to be retrieved.
    Returns:
        dict or None: A dictionary containing the user's debit transaction statistics by month if the request is successful,
        otherwise None.
    """
    # Call the user data endpoint from Model to retrieve the user transactions over time
    transactions = requests.get(url=f"{MODEL_API_ENDPOINT}/user/transaction/debit_stats", json={"user_id": user_id})
    
    # Check if the request was successful
    if transactions.status_code != 200:
        return None
    
    return transactions.json()

def get_credits_by_month(user_id):
    """
    Retrieve the user's credit transactions statistics by month.
    This function sends a GET request to the Model API to fetch the monthly credit transaction
    statistics for a given user.
    Args:
        user_id (str or int): The unique identifier of the user whose credit statistics are to be retrieved.
    Returns:
        dict or None: A dictionary containing the user's monthly credit statistics if the request is successful,
        otherwise None.
    """
    # Call the user data endpoint from Model to retrieve the user transactions over time
    transactions = requests.get(url=f"{MODEL_API_ENDPOINT}/user/transaction/credit_stats", json={"user_id": user_id})
    
    # Check if the request was successful
    if transactions.status_code != 200:
        return None
    
    return transactions.json()

def update_transaction(update_json):
    """
    Updates a transaction by sending a PUT request to the model API.
    Args:
        update_json (dict): A dictionary containing the transaction update data.
    Returns:
        bool: True if the update was successful (HTTP 200), False otherwise.
    """
    update = requests.put(url=f"{MODEL_API_ENDPOINT}/user/account/transaction", json=update_json)

    return update.status_code == 200

def create_transaction(create_json, user_id):
    """
    Creates a new transaction for a user by sending a POST request to the model API.
    Args:
        create_json (dict): The transaction data to be created.
        user_id (int or str): The ID of the user for whom the transaction is being created.
    Returns:
        bool: True if the transaction was created successfully (HTTP 200), False otherwise.
    """
    # Add the user_id to the create_json
    create_json["user_id"] = user_id

    # Call the user data endpoint from Model to create a new transaction
    create = requests.post(url=f"{MODEL_API_ENDPOINT}/user/account/transaction", json=create_json)

    return create.status_code == 201