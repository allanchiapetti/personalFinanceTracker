import os
from flask import Flask, Response, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from src.auth_user import auth_user

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

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
        access_token = create_access_token(identity=f"{user_data['user_id']}")
        response.set_cookie("access_token", access_token, httponly=True, secure=True)
        response.headers["Content-Type"] = "application/json"

    return response


@app.route("/test", methods=["GET"])
@jwt_required()
def test():
    """
    Test endpoint to verify the server is running.
    """
    return Response("Server is running", status=200, mimetype="text/plain")


