import hashlib
import os

class PasswordHash:
    def hash_password(self, password: str, salt: str) -> str:
        hashed_password = hashlib.pbkdf2_hmac('sha256', 
                                              password.encode('utf-8'), 
                                              salt.encode('utf-8'), 
                                              100000)

        return hashed_password.hex()
    
    def create_salt(self) -> str:
        salt = os.urandom(32)
        return salt.hex()