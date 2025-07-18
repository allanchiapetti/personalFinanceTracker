CREATE TABLE ACCOUNTS (
    ACCOUNT_ID INTEGER IDENTITY(1,1) PRIMARY KEY,
    USER_ID INTEGER NOT NULL FOREIGN KEY REFERENCES USERS(USER_ID),
    INSTITUTION VARCHAR(255) NOT NULL,
    ACCOUNT_NAME VARCHAR(255) NOT NULL,
    ACCOUNT_TYPE VARCHAR(255) NOT NULL CHECK (ACCOUNT_TYPE IN ('SAVINGS', 'CHECKING', 'CREDIT')),
    BALANCE REAL NOT NULL DEFAULT 0.0);