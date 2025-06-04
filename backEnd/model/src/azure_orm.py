import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

base = declarative_base()

class UserTable(base):
    __tablename__ = 'USERS'
    
    USER_ID = sa.Column(sa.INTEGER, primary_key=True)
    FIRST_NAME = sa.Column(sa.VARCHAR(255), nullable=False)
    LAST_NAME = sa.Column(sa.VARCHAR(255), nullable=False)
    EMAIL = sa.Column(sa.VARCHAR(255), nullable=False, unique=True)
    CREATED_AT = sa.Column(sa.DATETIME, nullable=False, server_default=sa.func.now())
    UPDATED_AT = sa.Column(sa.DATETIME, nullable=True, onupdate=sa.func.now())
    PASSWORD_HASH = sa.Column(sa.VARCHAR(255), nullable=False)
    PASSWORD_SALT = sa.Column(sa.VARCHAR(255), nullable=False)

    # Define the relationship to the AccountTable
    accounts = sa.orm.relationship("AccountTable", back_populates="user", cascade="all, delete-orphan")

class AccountTable(base):
    __tablename__ = 'ACCOUNTS'
    
    ACCOUNT_ID = sa.Column(sa.INTEGER, primary_key=True)
    USER_ID = sa.Column(sa.INTEGER, sa.ForeignKey('USERS.USER_ID'), nullable=False)
    INSTITUTION = sa.Column(sa.VARCHAR(255), nullable=False)
    ACCOUNT_NAME = sa.Column(sa.VARCHAR(255), nullable=False)
    ACCOUNT_TYPE = sa.Column(sa.VARCHAR(255), sa.CheckConstraint("ACCOUNT_TYPE in ('SAVINGS', 'CHECKING', 'CREDIT')"), nullable=False)
    BALANCE = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    #CREATED_AT = sa.Column(sa.DATETIME, nullable=False, server_default=sa.func.now())
    #UPDATED_AT = sa.Column(sa.DATETIME, nullable=True, onupdate=sa.func.now())
    
    # Define the relationship to the UserTable
    user = sa.orm.relationship("UserTable", back_populates="accounts")