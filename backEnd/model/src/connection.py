from sqlalchemy import create_engine, URL, text, orm
import pandas as pd
import os

SERVER = os.getenv("SERVER")
DATABASE_NAME = os.getenv("NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DRIVER = "{ODBC Driver 18 for SQL Server}" 


class Connection:
    def __init__(self):
        self.__conn_str = f'DRIVER={DRIVER};SERVER={SERVER};PORT=1433;DATABASE={DATABASE_NAME};UID={USERNAME};PWD={PASSWORD}'
        self.__conn_url = URL.create("mssql+pyodbc", query={"odbc_connect": self.__conn_str})


    def __create_engine(self):
        return create_engine(self.__conn_url)


    def create_session(self):
        """
        Create a new database session and return the connection.
        """
        engine = self.__create_engine()
        session = orm.sessionmaker(bind=engine)
        
        return session()

    
    def close_session(self, session):
        """
        Close the database session.
        """
        if session:
            session.close()