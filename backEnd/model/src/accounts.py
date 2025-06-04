from src.azure_orm import AccountTable, UserTable
from src.connection import Connection

import sqlalchemy as sa

class Accounts:
    def __init__(self):
        self.__conn = Connection()
    
    def get_user_accounts(self, user_id):
        """
        Get all accounts for a given user_id.
        If the user has no accounts, return an empty list.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for accounts associated with the user_id
            accounts = session.query(AccountTable).filter(AccountTable.USER_ID == user_id).all()

            # If accounts are found, return the account details
            if accounts:
                return [{"account_id": account.ACCOUNT_ID,
                         "institution": account.INSTITUTION,
                         "account_name": account.ACCOUNT_NAME,
                         "account_type": account.ACCOUNT_TYPE,
                         "balance": str(account.BALANCE)} for account in accounts], 200
            
            # If no accounts are found, return an empty list
            else:
                return [], 200
            
        # If any exception occurs, return an error message 
        except Exception as e:
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def create_account(self, user_id, institution, account_name, account_type, balance):
        """
        Create a new account for a given user_id with the provided details.
        If the account already exists, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Check if the account already exists for the user
            existing_account = session.query(AccountTable).filter(
                AccountTable.USER_ID == user_id,
                AccountTable.INSTITUTION == institution,
                AccountTable.ACCOUNT_NAME == account_name
            ).first()

            # If account already exists, return an error message
            if existing_account:
                return {"error": "Account already exists"}, 409
            
            # Create a new account instance and add it to the session
            new_account = AccountTable(
                USER_ID=user_id,
                INSTITUTION=institution,
                ACCOUNT_NAME=account_name,
                ACCOUNT_TYPE=account_type,
                BALANCE=balance
            )
            
            session.add(new_account)
            session.commit()
            
            return {"message": "Account created successfully", "account_id": new_account.ACCOUNT_ID}, 201
        
        # If any exception occurs, rollback the session and return an error message 
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)

    def update_account(self, account_id, user_id=None, institution=None, account_name=None, account_type=None, balance=None):
        """
        Update an existing account's details.
        If the account does not exist, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the account with the given account_id
            account = session.query(AccountTable).filter(AccountTable.ACCOUNT_ID == account_id).first()

            # If account is not found, return an error message
            if not account:
                return {"error": "Account not found"}, 404
            
            # Update the account details if provided
            if user_id is not None:
                account.USER_ID = user_id
            if institution is not None:
                account.INSTITUTION = institution
            if account_name is not None:
                account.ACCOUNT_NAME = account_name
            if account_type is not None:
                account.ACCOUNT_TYPE = account_type
            if balance is not None:
                account.BALANCE = balance
            
            session.commit()
            
            return {"message": "Account updated successfully"}, 200
        
        # If any exception occurs, rollback the session and return an error message 
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def delete_account(self, account_id):
        """
        Delete an account by its account_id.
        If the account does not exist, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the account with the given account_id
            account = session.query(AccountTable).filter(AccountTable.ACCOUNT_ID == account_id).first()

            # If account is not found, return an error message
            if not account:
                return {"error": "Account not found"}, 404
            
            # Delete the account and commit the changes
            session.delete(account)
            session.commit()
            
            return {"message": "Account deleted successfully"}, 200
        
        # If any exception occurs, rollback the session and return an error message 
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
