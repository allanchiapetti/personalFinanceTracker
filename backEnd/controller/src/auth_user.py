import os
import requests
from src.password_hash import PasswordHash

MODEL_API_ENDPOINT = os.getenv("MODEL_API_ENDPOINT")


def auth_user(email, password):
    """
    Authenticate a user by email and password.
    
    Args:
        email (str): The user's email address.
        password (str): The user's password.
    
    Returns:
        dict: A dictionary containing user information if authentication is successful, otherwise None.
    """
    # Call the user data endpoint from Model to retrieve user information
    user_data = requests.get(url=f"{MODEL_API_ENDPOINT}/user", json={"email": email})

    # Check if the request was successful
    if user_data.status_code != 200:
        return None
    
    else:
        # If the user data is found, create a PasswordHash object to calculate the hash
        user_data = user_data.json()
        user_id = user_data.get("user_id")
        password_salt = user_data.get("password_salt")

        hash_password = PasswordHash()
        hashed_password = hash_password.hash_password(password, password_salt)

        # Validate the user by checking the hashed password against the stored hash
        # Do this by calling the validate_password endpoint from Model
        validate_user = requests.post(f"{MODEL_API_ENDPOINT}/user/validate_password", 
                                      json={"user_id": user_id,
                                            "password_hash": hashed_password})

        # If the validation fails, return None
        if validate_user.status_code != 200:
            return None
        # If the validation is successful, return the user data
        else:
            return user_data
        
def create_user(email, password, first_name, last_name):
    """
    Creates a new user by hashing the provided password with a generated salt and sending the user data to the model API.
    Args:
        email (str): The user's email address.
        password (str): The user's plaintext password.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
    Returns:
        bool: True if the user was successfully created (HTTP 201), False otherwise.
    """

    # Create a PasswordHash object to calculate the hash
    hash_password = PasswordHash()
    
    # Create a salt for the password
    password_salt = hash_password.create_salt()

    # Hash the password with the salt
    hashed_password = hash_password.hash_password(password, password_salt)


    # Call the user data endpoint from Model to create a new user
    user_data = requests.post(url=f"{MODEL_API_ENDPOINT}/user", 
                              json={"email": email, 
                                    "password_hash": hashed_password, 
                                    "password_salt": password_salt,
                                    "first_name": first_name, 
                                    "last_name": last_name})
  
    return user_data.status_code == 201