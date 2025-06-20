import os
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, set_access_cookies
import jwt
from datetime import timedelta

class Token:
    def __init__(self):
        self.__JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    def create_token(self, user_id):
        token = jwt.encode({"user_id": str(user_id)}, self.__JWT_SECRET_KEY, algorithm="HS256")
        return token
    
    def validate_token(self, token):
        try:
            decoded_token = jwt.decode(token, self.__JWT_SECRET_KEY, algorithms=["HS256"])

            return decoded_token.get("user_id")
        except:
            return False



