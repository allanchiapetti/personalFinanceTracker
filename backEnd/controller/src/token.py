import os
import jwt
from datetime import timedelta

class Token:
    def __init__(self):
        self.__JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    def create_token(self, user_id):
        """
        Generates a JSON Web Token (JWT) for the specified user ID.

        Args:
            user_id (str or int): The unique identifier of the user for whom the token is being created.

        Returns:
            str: A JWT token string encoded with the user's ID.
        """
        token = jwt.encode({"user_id": str(user_id)}, self.__JWT_SECRET_KEY, algorithm="HS256")
        return token
    
    def validate_token(self, token):
        """
        Validates a JWT token and extracts the user ID.
        Args:
            token (str): The JWT token to be validated.
        Returns:
            str or bool: The user ID if the token is valid, otherwise False.
            False if token validation fails (e.g., invalid token, decoding error).
        """
        try:
            decoded_token = jwt.decode(token, self.__JWT_SECRET_KEY, algorithms=["HS256"])

            return decoded_token.get("user_id")
        except:
            return False



