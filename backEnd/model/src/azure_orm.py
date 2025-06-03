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
