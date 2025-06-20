import os
from flask import Flask, Response, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, set_access_cookies
from flask_cors import CORS, cross_origin

from src.auth_user import auth_user
from src.token import Token
from src.transactions import get_pending_transactions

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

#@cross_origin(supports_credentials=True, origins=["https://localhost" , "http://10.5.0.2:3000"])
@app.route("/transactions/pending", methods=["GET"])
def transactions_pending():
    """
    Test endpoint to verify the server is running.
    """
    token = request.cookies.get("jwt")
    user_id = request.args.get("user_id") 

    user_id = Token().validate_token(token)
    if user_id:
        response = make_response(jsonify(get_pending_transactions(str(user_id))), 200)
        response.headers["Content-Type"] = "application/json"

        return response
    else:
        return Response("Unauthorized", status=401, mimetype="text/plain")