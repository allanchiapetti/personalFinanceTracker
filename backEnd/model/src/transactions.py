from src.azure_orm import AccountTable, UserTable, TransactionTable
from src.connection import Connection

import sqlalchemy as sa

class Transaction:
    def __init__(self):
        self.__conn = Connection()
    
    def get_account_transactions(self, account_id):
        """
        Get all transactions for a given account_id.
        If the account has no transactions, return an empty list.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for transactions associated with the account_id
            transactions = session.query(TransactionTable).filter(TransactionTable.ACCOUNT_ID == account_id).all()

            # If transactions are found, return the transaction details
            if transactions:
                return [{"transaction_id": transaction.TRANSACTION_ID,
                         "category": transaction.CATEGORY,
                         "amount": str(transaction.AMOUNT),
                         "transaction_type": transaction.TRANSACTION_TYPE,
                         "transaction_date": transaction.TRANSACTION_DATE.isoformat(),
                         "description": transaction.DESCRIPTION,
                         "balance": str(transaction.BALANCE)} for transaction in transactions], 200
            
            # If no transactions are found, return an empty list
            else:
                return [], 200
            
        # If any exception occurs, return an error message 
        except Exception as e:
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def get_user_transactions(self, user_id):
        """
        Get all transactions for a given user_id.
        If the user has no transactions, return an empty list.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for accounts associated with the user_id
            user_transactions = session.query(TransactionTable)\
            .join(AccountTable, AccountTable.ACCOUNT_ID == TransactionTable.ACCOUNT_ID)\
            .join(UserTable, UserTable.USER_ID == AccountTable.USER_ID)\
            .filter(UserTable.USER_ID == user_id)\
            .all()

            # If transactions are found, return the transaction details
            if user_transactions:
                return [{"transaction_id": transaction.TRANSACTION_ID,
                         "category": transaction.CATEGORY,
                         "amount": str(transaction.AMOUNT),
                         "transaction_type": transaction.TRANSACTION_TYPE,
                         "transaction_date": transaction.TRANSACTION_DATE.isoformat(),
                         "description": transaction.DESCRIPTION,
                         "balance": str(transaction.BALANCE)} for transaction in user_transactions], 200      
            
            # If no transactions are found, return an empty list
            else:
                return [], 200     
            
        # If any exception occurs, return an error message 
        except Exception as e:
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def get_user_unpaid_transactions(self, user_id):
            """
            Get all transactions unpaid for a given user_id.
            If the user has no transactions, return an empty list.
            """
            session = self.__conn.create_session()
            
            try:
                # Query the database for accounts associated with the user_id
                user_transactions = session.query(TransactionTable)\
                                    .join(AccountTable, AccountTable.ACCOUNT_ID == TransactionTable.ACCOUNT_ID)\
                                    .join(UserTable, UserTable.USER_ID == AccountTable.USER_ID)\
                                    .filter(UserTable.USER_ID == user_id).where(TransactionTable.BALANCE != 0)\
                                    .order_by(TransactionTable.TRANSACTION_DATE.asc()).all()

                # If transactions are found, return the transaction details
                if user_transactions:
                    return [{"transaction_id": transaction.TRANSACTION_ID,
                            "account": transaction.account.ACCOUNT_NAME,
                            "category": transaction.CATEGORY,
                            "amount": round(transaction.AMOUNT, 2),
                            "transaction_type": transaction.TRANSACTION_TYPE,
                            "transaction_date": transaction.TRANSACTION_DATE.isoformat(),
                            "description": transaction.DESCRIPTION,
                            "balance": round(transaction.BALANCE, 2)} for transaction in user_transactions], 200

                # If no transactions are found, return an empty list
                else:
                    return [], 200     
                
            # If any exception occurs, return an error message 
            except Exception as e:
                return {"error": str(e)}, 500
            
            # Close the session after the operation
            finally:
                self.__conn.close_session(session)
    
    def create_transaction(self, account_id, category, amount, transaction_type, transaction_date, balance=None, description=None):
        """
        Create a new transaction for a given account_id with the provided details.
        If any required field is missing, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Create a new TransactionTable instance
            new_transaction = TransactionTable(
                ACCOUNT_ID=account_id,
                CATEGORY=category,
                AMOUNT=amount,
                TRANSACTION_TYPE=transaction_type,
                TRANSACTION_DATE=transaction_date,
                DESCRIPTION=description,
                BALANCE=balance if balance is not None else amount  # Default balance to amount if not provided
            )
            
            # Create the transaction in the database
            session.add(new_transaction)
            session.commit()
            
            return {"message": "Transaction created successfully", "transaction_id": new_transaction.TRANSACTION_ID}, 201
            
        # If any exception occurs, rollback the session and return an error message
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def update_transaction(self,  transaction_id, category=None, amount=None, balance=None, transaction_type=None, transaction_date=None, description=None):
        """
        Update an existing transaction with the provided details.
        If the transaction does not exist, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the transaction by transaction_id
            transaction = session.query(TransactionTable).filter(TransactionTable.TRANSACTION_ID == transaction_id).first()
            
            # If the transaction does not exist, return an error message
            if not transaction:
                return {"error": "Transaction not found"}, 404
            
            # Update the transaction with the provided keyword arguments
            if category is not None:
                transaction.CATEGORY = category
            if amount is not None:
                transaction.AMOUNT = amount
            if transaction_type is not None:
                transaction.TRANSACTION_TYPE = transaction_type
            if transaction_date is not None:
                transaction.TRANSACTION_DATE = transaction_date
            if description is not None:
                transaction.DESCRIPTION = description
            if balance is not None:
                transaction.BALANCE = balance
            
            # Commit the changes to the database
            session.commit()
            
            return {"message": "Transaction updated successfully"}, 200
            
        # If any exception occurs, rollback the session and return an error message
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)
    
    def delete_transaction(self, transaction_id):
        """
        Delete a transaction by transaction_id.
        If the transaction does not exist, return an error message.
        """
        session = self.__conn.create_session()
        
        try:
            # Query the database for the transaction by transaction_id
            transaction = session.query(TransactionTable).filter(TransactionTable.TRANSACTION_ID == transaction_id).first()
            
            # If the transaction does not exist, return an error message
            if not transaction:
                return {"error": "Transaction not found"}, 404
            
            # Delete the transaction from the database
            session.delete(transaction)
            session.commit()
            
            return {"message": "Transaction deleted successfully"}, 200
            
        # If any exception occurs, rollback the session and return an error message
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        
        # Close the session after the operation
        finally:
            self.__conn.close_session(session)