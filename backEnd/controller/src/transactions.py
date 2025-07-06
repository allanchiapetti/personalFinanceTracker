import os
import requests

MODEL_API_ENDPOINT = os.getenv("MODEL_API_ENDPOINT")

def get_pending_transactions(user_id):
    # Call the user data endpoint from Model to retrieve the user pending transactions
    pending_transactions = requests.get(url=f"{MODEL_API_ENDPOINT}/user/transaction/unpaid", json={"user_id": user_id})

    # Check if the request was successful
    if pending_transactions.status_code != 200:
        return None
    else:
        return pending_transactions.json()

def get_spending_by_month(user_id):
    # Call the user data endpoint from Model to retrieve the user transactions over time
    transactions = requests.get(url=f"{MODEL_API_ENDPOINT}/user/transaction/debit_stats", json={"user_id": user_id})
    
    # Check if the request was successful
    if transactions.status_code != 200:
        return None
    
    return transactions.json()

def get_credits_by_month(user_id):
    # Call the user data endpoint from Model to retrieve the user transactions over time
    transactions = requests.get(url=f"{MODEL_API_ENDPOINT}/user/transaction/credit_stats", json={"user_id": user_id})
    
    # Check if the request was successful
    if transactions.status_code != 200:
        return None
    
    return transactions.json()

def update_transaction(update_json):
    update = requests.put(url=f"{MODEL_API_ENDPOINT}/user/account/transaction", json=update_json)

    return update.status_code == 200

def create_transaction(create_json, user_id):
    # Add the user_id to the create_json
    create_json["user_id"] = user_id

    # Call the user data endpoint from Model to create a new transaction
    create = requests.post(url=f"{MODEL_API_ENDPOINT}/user/account/transaction", json=create_json)

    return create.status_code == 200