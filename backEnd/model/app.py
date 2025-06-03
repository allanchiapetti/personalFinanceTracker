from flask import Flask, Response, request, make_response, jsonify
from src.users import User
import json

app = Flask(__name__)
user_obj = User()

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
            data["first_name"],
            data["last_name"],
            data["email"],
            data["password_hash"],
            data["password_salt"]
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
            return Response(json.dumps({"error": "User ID is required"}), status=400, mimetype="application/json")
        
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