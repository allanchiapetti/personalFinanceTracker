import os
from flask import Flask, Response, request, make_response, jsonify
#from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, set_access_cookies
from flask_cors import CORS, cross_origin

from src.auth_user import auth_user, create_user
from src.token import Token
from src.transactions import get_pending_transactions, update_transaction, create_transaction, get_spending_by_month, get_credits_by_month
from src.accounts import get_user_accounts, update_account, delete_account, create_account

app = Flask(__name__)

#jwt = JWTManager(app)

#app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
#app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

#jwt = JWTManager(app)

CORS(app, supports_credentials=True, origins=["https://localhost", "http://10.5.0.2:3000"]) # MUST BE ADJUSTED FOR PRODUCTION

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = 'https://localhost'  # MUST BE ADJUSTED FOR PRODUCTION
    return response


# User authentication endpoint
@app.route("/auth", methods=["POST"])
def auth():
    """
    Authenticates a user based on provided email and password.
    Expects a JSON payload with "email" and "password" fields in the request body.
    If authentication is successful, returns user data and sets a JWT token as a cookie.
    If authentication fails or input is invalid, returns an appropriate error response.
    Returns:
        Response: A Flask response object containing either user data (on success) or an error message (on failure).
    """
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return make_response(jsonify({"error": "Invalid input"}), 400)

    email = data["email"]
    password = data["password"]

    user_data = auth_user(email=email, password=password)

    # If authentication fails, return an error response
    if user_data is None:
        response = make_response(jsonify({"error": "Authentication failed"}), 401)
        response.headers["Content-Type"] = "application/json"

    # If authentication is successful, return user data
    else:
        response = make_response(jsonify(user_data), 200)
        access_token = Token().create_token(user_id=user_data["user_id"])
        
        response.set_cookie("jwt", access_token, httponly=False, secure=True, samesite="None", path="/")

    return response

@app.route("/user", methods=["POST"])
def user():
    """
    Handles user creation by processing JSON input containing 'email', 'password', 'first_name', and 'last_name'.
    Validates input data, creates a new user, and returns the created user data as a JSON response with status 201.
    Returns an error response with appropriate status code if input is invalid or user creation fails.
    Returns:
        Response: JSON response containing user data and HTTP status 201 on success,
                  or error message with status 400 or 500 on failure.
    """
    data = request.get_json()
    if not data or "email" not in data or "password" not in data or "first_name" not in data or "last_name" not in data:
        return make_response(jsonify({"error": "Invalid input"}), 400)

    email = data["email"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]

    user_data = create_user(email=email, password=password, first_name=first_name, last_name=last_name)

    if not user_data:
        return make_response(jsonify({"error": "User creation failed"}), 500)

    response = make_response(jsonify(user_data), 201)

    return response


@app.route("/transactions/pending", methods=["GET"])
def transactions_pending():
    """
    Handles the retrieval of pending transactions for the authenticated user.
    Authentication:
        - Requires a valid JWT token in the request cookies.
        - Returns 401 Unauthorized if the token is missing or invalid.
    Returns:
        flask.Response: A JSON response with the list of pending transactions and a 200 status code if authenticated,
                        otherwise a plain text response with a 401 status code.
    """
    token = request.cookies.get("jwt")

    user_id = Token().validate_token(token)
    if user_id:
        response = make_response(jsonify(get_pending_transactions(str(user_id))), 200)
        response.headers["Content-Type"] = "application/json"

        return response
    else:
        return Response("Unauthorized", status=401, mimetype="text/plain")

@app.route("/transactions", methods=["PUT", "POST"])
def transactions():
    """
    Handles HTTP requests for creating and updating user transactions.
    This function processes PUT and POST requests:
        - PUT: Updates an existing transaction with data from the request JSON body.
        - POST: Creates a new transaction with data from the request JSON body and the authenticated user ID.
    Authentication:
        - Requires a valid JWT token in the request cookies.
        - Returns 401 Unauthorized if the token is missing or invalid.
    Returns:
        Response: 
            - 200 OK on successful creation or update.
            - 500 Internal Server Error on failure to create or update.
            - 401 Unauthorized if authentication fails.
    """
    token = request.cookies.get("jwt")

    user_id = Token().validate_token(token)
    if user_id:

        if request.method == "PUT":
            update = update_transaction(request.get_json())
            
            if update:
                return Response(status=200)  
            
            return Response(status=500)
        
        if request.method == "POST":
            create = create_transaction(request.get_json(), user_id)

            if create:
                return Response(status=200)

            return Response(status=500)
        
    else:
        return Response("Unauthorized", status=401, mimetype="text/plain")
    
@app.route("/accounts", methods=["GET", "PUT", "DELETE", "POST"])
def accounts():
    """
    Handles account-related HTTP requests for the authenticated user.
    This function supports the following HTTP methods:
        - GET:    Retrieves all accounts associated with the authenticated user.
        - POST:   Creates a new account for the authenticated user using provided JSON data.
        - PUT:    Updates an existing account with provided JSON data.
        - DELETE: Deletes an account specified in the provided JSON data.
    Authentication:
        - Requires a valid JWT token in the request cookies.
        - Returns 401 Unauthorized if the token is missing or invalid.
    Returns:
        - 200 OK: On successful retrieval, creation, update, or deletion of accounts.
        - 404 Not Found: If no accounts are found for the user (GET).
        - 401 Unauthorized: If the JWT token is missing or invalid.
        - 500 Internal Server Error: If an error occurs during account creation, update, or deletion.
    """
    token = request.cookies.get("jwt")

    user_id = Token().validate_token(token)
    if user_id:

        if request.method == "GET":
            user_accounts = get_user_accounts(user_id)
            
            if user_accounts is None:
                return Response("No accounts found", status=404, mimetype="text/plain")
            
            return jsonify(user_accounts), 200
        
        if request.method == "PUT":
            update = update_account(request.get_json())
            
            if update:
                return Response(status=200)
            
            return Response(status=500)
        
        if request.method == "DELETE":
            delete = delete_account(request.get_json())
            
            if delete:
                return Response(status=200)
            
            return Response(status=500)
    
        if request.method == "POST":
            create = create_account(request.get_json(), user_id)

            if create:
                return Response(status=200)

            return Response(status=500)

    else:
        return Response("Unauthorized", status=401, mimetype="text/plain")
    
@app.route("/accounts/debit_stats", methods=["GET"])
def debit_status():
    """
    Handles the retrieval of a user's monthly spending status.
    Authentication:
    - Requires a valid JWT token in the request cookies.
    - Returns 401 Unauthorized if the token is missing or invalid.
    Authentication:
        - Requires a valid JWT token in the request cookies.
        - Returns 401 Unauthorized if the token is missing or invalid..
    Returns:
        Response: A JSON response containing the spending data by month with a 200 status code,
                  or a plain text response with a 404 status code if no transactions are found.
    """

    token = request.cookies.get("jwt")

    user_id = Token().validate_token(token)
    if user_id:
        spending_by_month = get_spending_by_month(user_id)

        if spending_by_month is None:
            return Response("No transactions found", status=404, mimetype="text/plain")

        return jsonify(spending_by_month), 200
    
@app.route("/accounts/credit_stats", methods=["GET"])
def credit_stats():
    """
    Handles the retrieval of credit statistics for the authenticated user.
    Authentication:
        - Requires a valid JWT token in the request cookies.
        - Returns 401 Unauthorized if the token is missing or invalid.
    Returns:
        Response: A JSON response containing the credits by month and a 200 status code if successful,
                  or a plain text response with a 404 status code if no transactions are found.
    """
    token = request.cookies.get("jwt")

    user_id = Token().validate_token(token)
    if user_id:
        credits_by_month = get_credits_by_month(user_id)

        if credits_by_month is None:
            return Response("No transactions found", status=404, mimetype="text/plain")

        return jsonify(credits_by_month), 200