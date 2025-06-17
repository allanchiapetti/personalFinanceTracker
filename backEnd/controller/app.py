import os
from flask import Flask, Response, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, set_access_cookies
from flask_cors import CORS
import ssl

from src.auth_user import auth_user

app = Flask(__name__)

jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
#app.config["JWT_COOKIE_SECURE"] = True
#app.config["JWT_COOKIE_SAMESITE"] = "None"
#app.config["JWT_COOKIE_CSRF_PROTECT"] = True
#app.config["JWT_ACCESS_COOKIE_PATH"] = "/api/"
app.config["JWT_REFRESH_COOKIE_PATH"] = "/token/refresh"

jwt = JWTManager(app)

CORS(app, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = 'https://localhost.com'  # Adjust as needed
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
        access_token = create_access_token(identity=str(user_data["user_id"]))
        response.set_cookie("jwt", access_token, httponly=False, secure=True,  samesite="None")

    return response


@app.route("/test", methods=["GET"])
def test():
    """
    Test endpoint to verify the server is running.
    """
    token = request.cookies.get("jwt")
    if not token:
        return Response("No token", status=401, mimetype="text/plain")
    else:
        try:
            jwt.decode_token(token)
        except Exception as e:
            return Response("Unauthorized", status=401, mimetype="text/plain")
    
    return Response("Server is running", status=200, mimetype="text/plain")


