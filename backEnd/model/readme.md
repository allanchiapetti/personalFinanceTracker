# Camada de dados – `backEnd/model/`
## Requisitos

- Python 3.13+
- Flask
- SQLAlchemy
- Gunicorn
- Microsoft ODBC Driver for SQL Server
- Docker

## Arquivos e Funcionalidades

### connection.py
Gerencia a conexão com a instância do banco de dados no cloud

### azure_orm.py
Define o modelo de dados relacional da aplicação usando SQLAlchemy

### users.py
Contém as funções de leitura + CRUD para dados de usuário

### transactions.py
Contém as funções de leitura + CRUD para dados de transações

### accounts.py
Contém as funções de leitura + CRUD para dados de contas

#### Endpoints

- `GET /user`  
  Retorna os dados do usuário

  **Exemplo**:
  ```json
  {
    "email": "usuario@example.com"
  }
- `POST /user`  
  Cria um novo usuário

  **Exemplo**:
  ```json
  {
    "email": "usuario@example.com",
    "first_name": "Usuário",
    "last_name": "de Test",
    "password_hash": "454f7c552baf1daa7c111e0492cb3474e7b2071b2f671a18c845b853ebd8f94b",
    "password_salt": "d2bb51cc14c459d9c4e003117d622687a1f321bf255c87844a437522d0c522d0"
  }
- `PUT /user`  
  Atualiza os dados de um usuário

  **Exemplo**:
  ```json
  {
    "user_id": "1",
    "email": "usuario@example.com",
    "first_name": "Usuário",
    "last_name": "de Test",
    "password_hash": "454f7c552baf1daa7c111e0492cb3474e7b2071b2f671a18c845b853ebd8f94b",
    "password_salt": "d2bb51cc14c459d9c4e003117d622687a1f321bf255c87844a437522d0c522d0"
  }
  user_id é obrigatório. 
  Os demais campos serão atualizados se passados na chamada, caso contrário será mantido o valor salvo.
- `DELETE /user`  
  Deleta um usuário

  **Exemplo**:
  ```json
  {
    "user_id": "1"
  }
- `POST /user/validate_password`  
  Valida a senha de um usuário

  **Exemplo**:
  ```json
  {
    "user_id": "1",
    "password_hash": "454f7c552baf1daa7c111e0492cb3474e7b2071b2f671a18c845b853ebd8f94b"
  }
- `GET /user/account`  
  Retorna todas as contas do usuário

  **Exemplo**:
  ```json
  {
    "user_id": "1"
  }
- `POST /user/account`  
  Cria uma nova conta associada a uma conta de um usuário

  **Exemplo**:
  ```json
  {
    "user_id": "1", 
    "institution": "Banco", 
    "account_name": "Conta", 
    "account_type": "Savings", 
    "balance": "5000"
  }
- `PUT /user/account`  
  Altera dados de uma conta.
  
  **Exemplo**:
  ```json
  {
    "account_id": "1",
    "institution": "Extra",
    "account_name": "300",
    "account_type": "Debit",
    "balance": "280"
  }
  account_id é obrigatório. 
  Os demais campos serão atualizados se passados na chamada, caso contrário será mantido o valor salvo.
- `DELETE /user/account`  
  Deleta a conta
  
  **Exemplo**:
  ```json
  {
    "account_id": "1"
  }
- `GET /user/transaction`  
  Retorna todas as transações do usuário
  
  **Exemplo**:
  ```json
  {
    "user_id": "1"
  }
- `GET /user/transaction/unpaid`  
  Retorna todas as transações do usuário que tenha saldo diferente de 0
  
  **Exemplo**:
  ```json
  {
    "user_id": "1"
  }
- `GET /user/transaction/credit_stats`  
  Agrega o valor das transações classificadas como crédito do usuário por mês e retorna os dados em um json
  
  **Exemplo**:
  ```json
  {
    "user_id": "1"
  }
- `GET /user/transaction/debit_stats`  
  Agrega o valor das transações classificadas como débito do usuário por mês e retorna os dados em um json
  
  **Exemplo**:
  ```json
  {
    "user_id": "1"
  }
- `GET /user/account/transaction`  
  Retorna todas as transações de uma conta
  
  **Exemplo**:
  ```json
  {
    "account_id": "1"
  }
- `POST /user/account/transaction`  
  Cria uma nova transação associada em uma conta
  
  **Exemplo**:
  ```json
  {
    "account_id": "1",
    "category": "Energia",
    "amount": "250",
    "transaction_type": "Debit",
    "transaction_date": "2024-12-15",
    "description": "Test transação"
  }
- `PUT /user/account/transaction`  
  Cria uma nova transação associada em uma conta
  
  **Exemplo**:
  ```json
  {
    "transaction_id": "1",
    "category": "Energia",
    "amount": "250",
    "transaction_type": "Debit",
    "transaction_date": "2024-12-15",
    "description": "Test transação",
    "balance": "150"
  }
  transaction_id é obrigatório. 
  Os demais campos serão atualizados se passados na chamada, caso contrário será mantido o valor salvo.
- `DELETE /user/account/transaction`  
  Deleta uma transação
  
  **Exemplo**:
  ```json
  {
    "transaction_id": "1"
  }