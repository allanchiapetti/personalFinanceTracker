import hashlib
import os

class PasswordHash:
    def hash_password(self, password: str, salt: str) -> str:
        """
        Hashes a password using PBKDF2 HMAC with SHA-256.
        Args:
            password (str): The plain text password to hash.
            salt (str): The salt to use for hashing.
        Returns:
            str: The resulting hashed password as a hexadecimal string.
        """
        hashed_password = hashlib.pbkdf2_hmac('sha256', 
                                              password.encode('utf-8'), 
                                              salt.encode('utf-8'), 
                                              100000)

        return hashed_password.hex()
    
    def create_salt(self) -> str:
        """
        Generates a cryptographically secure random salt.

        Returns:
            str: A hexadecimal string representation of a 32-byte random salt.
        """
        salt = os.urandom(32)
        return salt.hex()