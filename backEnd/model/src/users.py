from src.azure_orm import UserTable
from src.connection import Connection

import sqlalchemy as sa

class User:
    def __init__(self):
        self.__conn = Connection()

    def get_user_data(self, email):
        """
        Get the user_id for a given email.
        If the user is not found, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the user with the given email
            user = session.query(UserTable).filter(UserTable.EMAIL == email).first()

            # If user is found, return the user details
            if user:
                return {"user_id": user.USER_ID,
                        "first_name": user.FIRST_NAME,
                        "last_name": user.LAST_NAME,
                        "password_salt": user.PASSWORD_SALT,
                        "created_at": user.CREATED_AT,
                        "updated_at": user.UPDATED_AT}, 200
            
            # If user is not found, return an error message
            else:
                return {"error": "User not found"}, 404
            
        # If any exception occurs, return an error message 
        except Exception as e:
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def create_user(self, first_name, last_name, email, password_hash, password_salt):
        """
        Create a new user with the provided details.
        If the user already exists, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the user with the given email
            existing_user = session.query(UserTable).filter(UserTable.EMAIL == email).first()

            # If user already exists, return an error message
            if existing_user:
                return {"error": "User already exists"}, 409
            
            # Create a new user instance and add it to the session
            new_user = UserTable(
                FIRST_NAME=first_name,
                LAST_NAME=last_name,
                EMAIL=email,
                PASSWORD_HASH=password_hash,
                PASSWORD_SALT=password_salt
            )

            # Create the user and commit the changes to the database
            session.add(new_user)
            session.commit()
            
            return {"message": "User created successfully", "user_id": new_user.USER_ID}, 201
        
        # If any exception occurs, rollback the session and return an error message
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def update_user(self, user_id, first_name=None, last_name=None, email=None, password_hash=None, password_salt=None):
        """
        Update an existing user's details.
        If the user does not exist, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the user with the given user_id
            user = session.query(UserTable).filter(UserTable.USER_ID == user_id).first()

            # If user is not found, return an error message
            if not user:
                return {"error": "User not found"}, 404
            
            # Update the user according to the provided fields
            if first_name:
                user.FIRST_NAME = first_name
            if last_name:
                user.LAST_NAME = last_name
            if email:
                user.EMAIL = email
            if password_hash:
                user.PASSWORD_HASH = password_hash
            if password_salt:
                user.PASSWORD_SALT = password_salt  

            # Update the updated_at field with the current timestamp
            user.UPDATED_AT = sa.func.now() 
            
            # Commit the changes to the database
            session.commit()
            return {"message": "User updated successfully"}, 200
        
        # If any exception occurs, rollback the session and return an error message
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def delete_user(self, user_id):
        """
        Delete a user by user_id.
        If the user does not exist, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the user with the given user_id
            user = session.query(UserTable).filter(UserTable.USER_ID == user_id).first()

            # If user is not found, return an error message
            if not user:
                return {"error": "User not found"}, 404
            
            # Delete the user and commit the changes
            session.delete(user)
            session.commit()
            return {"message": "User deleted successfully"}, 200
        
        # If any exception occurs, rollback the session and return an error message
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def validate_password(self, user_id, password_hash):
        """
        Validate the user's password.
        If the user is not found or the password does not match, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the user with the given user_id
            user = session.query(UserTable).filter(UserTable.USER_ID == user_id).first()

            # If user is not found, return an error message
            if not user:
                return {"error": "User not found"}, 404
            
            # Check if the provided password hash matches the stored password hash
            if user.PASSWORD_HASH == password_hash:
                return {"message": "Password is valid"}, 200
            else:
                return {"error": "Invalid password"}, 401
        
        # If any exception occurs, return an error message
        except Exception as e:
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)