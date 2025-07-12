# Camada de controle – `backEnd/controller/`
## Requisitos

- Python 3.10+
- Flask
- JWT (PyJWT)
- Postman (para testes)

<h1>Requisitos</h1>
    <ul>
        <li>Python 3.13+</li>
        <li>Flask</li>
        <li>JWT (PyJWT)</li>
        <li>Postman (para testes)</li>
    </ul>

## Arquivos e Funcionalidades

### `auth_user_.py`

Gerencia autenticação e registro de usuários.

### `password_hash.py`

Implementa a função hashing e a criação de SALT randomizado

### `token.py`

Responsável pela criação do token no processo de login e da validação do token recebido nas chamadas do frontend
<br>Se o token é validado com sucesso, retorna o user_id que permitirá identificar o usuário para as demais ações

### `accounts.py`

Gerencia a leitura, criação, atualização e remoção de contas vinculadas ao usuário.

### `transactions.py`

Gerencia a leitura, criação e atualização de transações vinculadas ao usuário.

#### Endpoints

- `POST /auth`  
  Autentica o usuário e retorna um token JWT + os dados do usuário.

  **Exemplo**:
  ```json
  {
    "email": "usuario@example.com",
    "password": "senha123"
  }

- `POST /user`  
  Cria um usuário e retorna os dados do usuário criado.

  **Exemplo**:
  ```json
  {
    "email": "usuario@example.com",
    "password": "senha123",
    "first_name": "Usuário",
    "last_name": "Test"
  }

- `GET /transactions/pending`  
  <b>Obtém o user_id a partir do token JWT</b>
  <br>Retorna as transações pendentes (com saldo diferente de 0) do usuário

- `POST /transactions`  
  Cria uma nova transação associada a uma conta de um usuário

  **Exemplo**:
  ```json
  {
    "account_id": "1",
    "category": "Extra",
    "amount": "300",
    "transaction_type": "Debit",
    "transaction_date": "2025-06-19T20:30:22",
    "description": "Test 2"
  }

- `PUT /transactions`  
  Altera dados de uma transação.
  
  **Exemplo**:
  ```json
  {
    "transaction_id": "1",
    "category": "Extra",
    "amount": "300",
    "transaction_type": "Debit",
    "transaction_date": "2025-06-19T20:30:22",
    "description": "Test 2",
    "balance": "280"
  }
  transaction_id é obrigatório. 
  Os demais campos serão atualizados se passados na chamada, caso contrário será mantido o valor salvo.

- `GET /accounts`  
  <b>Obtém o user_id a partir do token JWT</b>
  <br>Retorna todas as contas do usuário

- `POST /accounts`  
  Cria uma nova conta associada a uma conta de um usuário

  **Exemplo**:
  ```json
  {
    "user_id": "1", 
    "institution": "Banco", 
    "account_name": "Conta", 
    "account_type": "Corrent", 
    "balance": "150.50"
  }

- `PUT /accounts`
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

- `DELETE /accounts`
  Deleta uma conta.
  
  **Exemplo**:
  ```json
  {
    "account_id": "1"
  }

- `GET /accounts/debit_stats`  
  <b>Obtém o user_id a partir do token JWT</b>
  <br>Retorna todas as transações do usuário classificadas como débito

- `GET /accounts/credit_stats`  
  <b>Obtém o user_id a partir do token JWT</b>
  <br>Retorna todas as transações do usuário classificadas como crédito