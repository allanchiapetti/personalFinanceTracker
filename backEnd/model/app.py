from flask import Flask, Response, request, make_response, jsonify
from src.users import User
from src.accounts import Account
from src.transactions import Transaction
import json

from datetime import datetime

app = Flask(__name__)
user_obj = User()
accounts_obj = Account()
transaction_obj = Transaction()

# User API Endpoints
@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == "GET":
        """
        Get the user data for a given email.
        If the email is missing, return an error message.
        """
        # Get JSON data from the request
        data = request.get_json() 

        # Extract email from the JSON data
        email = data.get("email") if data else None

        if not email: # If email is not provided, return an error response
            response = make_response(jsonify({"error": "Email is required"}), 400)
            response.headers["Content-Type"] = "application/json"

            return response
        
        # Call the method to get user_id based on email and return the response
        get_user_response, status_code = user_obj.get_user_data(email)
        
        # Return the response
        response = make_response(jsonify(get_user_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "POST":
        """
        Create a new user with the provided details.
        If any required field is missing, return an error message.
        """
        # Get JSON data from the request
        data = request.get_json()

        # List the required fields for user creation
        required_fields = ["first_name", "last_name", "email", "password_hash", "password_salt"]
        
        # Check if all required fields are present in the JSON data
        if not all(field in data for field in required_fields):
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response
                
        # Call the method to create a new user
        create_user_response, status_code = user_obj.create_user(
            data.get("first_name"),
            data.get("last_name"),
            data.get("email"),
            data.get("password_hash"),
            data.get("password_salt")
        )

        # Return the response
        response = make_response(jsonify(create_user_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response

    elif request.method == "PUT":
        """
        Update user details.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "user_id" not in data:
            response = make_response({"error": "Missing user id"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        update_user_response, status_code = user_obj.update_user(
            data.get("user_id"),
            data.get("first_name"),
            data.get("last_name"),
            data.get("email"),
            data.get("password_hash"),
            data.get("password_salt")
        )

        # Return the response
        response = make_response(jsonify(update_user_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "DELETE":
        """
        Delete a user based on user_id.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "user_id" not in data:
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response
        
        delete_user_response, status_code = user_obj.delete_user(data["user_id"])

        # Return the response
        response = make_response(jsonify(delete_user_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response

# Validate User Password API Endpoint
@app.route("/user/validate_password", methods=["GET"])
def validate_password():
    """
    Validate the password for a given user.
    """
    # Get JSON data from the request
    data = request.get_json()
    
    # List the required fields for password validation
    required_fields = ["user_id", "password_hash"]
        
    # Check if all required fields are present in the JSON data
    if not all(field in data for field in required_fields):
        response = make_response({"error": "Missing required fields"}, 400)
        response.headers["Content-Type"] = "application/json"
        return response

    # Call the method to validate the password
    is_valid, status_code = user_obj.validate_password(user_id=data.get("user_id"), 
                                                       password_hash=data.get("password_hash"))

    # Return the response
    response = make_response(jsonify({"is_valid": is_valid}), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

# Accounts API Endpoints
@app.route("/user/account", methods=["GET", "POST", "PUT", "DELETE"])
def user_accounts():
    if request.method == "GET":
        """
        Get all accounts for a given user_id.
        If the user has no accounts, return an empty list.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "user_id" not in data:
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        user_id = data.get("user_id")
        
        # Call the method to get user accounts
        accounts_response, status_code = accounts_obj.get_user_accounts(user_id)

        # Return the response
        response = make_response(jsonify(accounts_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "POST":
        """
        Create a new account for a given user_id with the provided details.
        If any required field is missing, return an error message.
        """
        # Get JSON data from the request
        data = request.get_json()

        # List the required fields for account creation
        required_fields = ["user_id", "institution", "account_name", "account_type", "balance"]
        
        # Check if all required fields are present in the JSON data
        if not all(field in data for field in required_fields):
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        # Call the method to create a new account
        create_account_response, status_code = accounts_obj.create_account(
            user_id=data.get("user_id"),
            institution=data.get("institution"),
            account_name=data.get("account_name"),
            account_type=data.get("account_type"),
            balance=data.get("balance")
        )

        # Return the response
        response = make_response(jsonify(create_account_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "PUT":
        """
        Update an existing account for a given user_id with the provided details.
        If any required field is missing, return an error message.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "account_id" not in data:
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        # Call the method to update an account
        update_account_response, status_code = accounts_obj.update_account(
            account_id=data.get("account_id"),
            institution=data.get("institution"),
            account_name=data.get("account_name"),
            account_type=data.get("account_type"),
            balance=data.get("balance")
        )

        # Return the response
        response = make_response(jsonify(update_account_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "DELETE":
        """
        Delete an account based on account_id.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "account_id" not in data:
            return Response(json.dumps({"error": "Account ID is required"}), status=400, mimetype="application/json")
        
        delete_account_response, status_code = accounts_obj.delete_account(data.get("account_id"))

        # Return the response
        response = make_response(jsonify(delete_account_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response

# Transactions API Endpoints
@app.route("/user/transaction", methods=["GET"])
def user_transaction():
    """
    Get all transactions for a given user_id.
    If the user has no transactions, return an empty list.
    """
    # Get JSON data from the request
    data = request.get_json()

    if not data or "user_id" not in data:
        response = make_response({"error": "Missing required fields"}, 400)
        response.headers["Content-Type"] = "application/json"
        return response

    user_id = data.get("user_id")
    
    # Call the method to get user transactions
    transactions_response, status_code = transaction_obj.get_user_transactions(user_id)

    # Return the response
    response = make_response(jsonify(transactions_response), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/user/transaction/unpaid", methods=["GET"])
def user_transaction_unpaid():
    """
    Get all unpaid transactions for a given user_id.
    If the user has no unpaid transactions, return an empty list.
    """
    # Get JSON data from the request
    data = request.get_json()

    if not data or "user_id" not in data:
        response = make_response({"error": "Missing required fields"}, 400)
        response.headers["Content-Type"] = "application/json"
        return response

    user_id = data.get("user_id")
    
    # Call the method to get user unpaid transactions
    unpaid_transactions_response, status_code = transaction_obj.get_user_unpaid_transactions(user_id)

    # Return the response
    response = make_response(jsonify(unpaid_transactions_response), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/user/account/transaction", methods=["GET", "POST", "PUT", "DELETE"])
def user_account_transaction():
    if request.method == "GET":
        """
        Get all transactions for a given account_id.
        If the account has no transactions, return an empty list.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "account_id" not in data:
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        account_id = data.get("account_id")
        
        # Call the method to get account transactions
        transactions_response, status_code = transaction_obj.get_account_transactions(account_id)

        # Return the response
        response = make_response(jsonify(transactions_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "POST":
        """
        Create a new transaction for a given account_id with the provided details.
        If any required field is missing, return an error message.
        """
        # Get JSON data from the request
        data = request.get_json()

        # List the required fields for transaction creation
        required_fields = ["account_id", "category", "amount", "transaction_type", "transaction_date"]
        
        # Check if all required fields are present in the JSON data
        if not all(field in data for field in required_fields):
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        # Call the method to create a new transaction
        create_transaction_response, status_code = transaction_obj.create_transaction(
            account_id=data.get("account_id"),
            category=data.get("category"),
            amount=data.get("amount"),
            transaction_type=data.get("transaction_type"),
            transaction_date=datetime.strptime(data.get("transaction_date"), "%Y-%m-%dT%H:%M:%S"),
            paid=data.get("paid"),
            description=data.get("description")
        )

        # Return the response
        response = make_response(jsonify(create_transaction_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "PUT":
        """
        Update an existing transaction for a given account_id with the provided details.
        If any required field is missing, return an error message.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "transaction_id" not in data:
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response

        # Call the method to update a transaction
        update_transaction_response, status_code = transaction_obj.update_transaction(
            transaction_id=data.get("transaction_id"),
            category=data.get("category"),
            amount=data.get("amount"),
            transaction_type=data.get("transaction_type"),
            transaction_date=datetime.strptime(data.get("transaction_date"), "%Y-%m-%dT%H:%M:%S"),
            paid=data.get("paid"),
            description=data.get("description")
        )

        # Return the response
        response = make_response(jsonify(update_transaction_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response
    
    elif request.method == "DELETE":
        """
        Delete a transaction based on transaction_id.
        """
        # Get JSON data from the request
        data = request.get_json()

        if not data or "transaction_id" not in data:
            response = make_response({"error": "Missing required fields"}, 400)
            response.headers["Content-Type"] = "application/json"
            return response
        
        delete_transaction_response, status_code = transaction_obj.delete_transaction(data.get("transaction_id"))

        # Return the response
        response = make_response(jsonify(delete_transaction_response), status_code)
        response.headers["Content-Type"] = "application/json"
        return response