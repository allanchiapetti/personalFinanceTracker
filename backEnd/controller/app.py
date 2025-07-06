import os
from flask import Flask, Response, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, set_access_cookies
from flask_cors import CORS, cross_origin

from src.auth_user import auth_user, create_user
from src.token import Token
from src.transactions import get_pending_transactions, update_transaction, create_transaction, get_spending_by_month, get_credits_by_month
from src.accounts import get_user_accounts, update_account, delete_account, create_account

app = Flask(__name__)

jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
#app.config["JWT_COOKIE_SECURE"] = True
#app.config["JWT_COOKIE_SAMESITE"] = "None"
#app.config["JWT_COOKIE_CSRF_PROTECT"] = True
#app.config["JWT_ACCESS_COOKIE_PATH"] = "/api/"
#app.config["JWT_REFRESH_COOKIE_PATH"] = "/token/refresh"

jwt = JWTManager(app)

CORS(app, supports_credentials=True, origins=["https://localhost", "http://10.5.0.2:3000"])

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = 'https://localhost'  # Adjust as needed
    return response


# User authentication endpoint
@app.route("/auth", methods=["POST"])
def auth():
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
    Endpoint to create a new user.
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


#@cross_origin(supports_credentials=True, origins=["https://localhost" , "http://10.5.0.2:3000"])
@app.route("/transactions/pending", methods=["GET"])
def transactions_pending():
    """
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
    """
    token = request.cookies.get("jwt")

    user_id = Token().validate_token(token)
    if user_id:
        credits_by_month = get_credits_by_month(user_id)

        if credits_by_month is None:
            return Response("No transactions found", status=404, mimetype="text/plain")

        return jsonify(credits_by_month), 200