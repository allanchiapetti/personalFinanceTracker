# Frontend – Financial Tracker PUC

Este diretório contém o código-fonte do frontend da aplicação de controle financeiro pessoal, desenvolvida como parte de um projeto acadêmico. 
A aplicação foi construída utilizando o framework **Next.js**

##  Tecnologias Utilizadas

- **Next.js**
- **React**
- **JavaScript / JSX**
- **TaiwWind**
- **Axios**

## ⚙️ Estrutura de Diretórios
```
financial_tracker_puc/ 
    ├── public/              
    ├── src
        ├── pages/  
           ├── api/
           ├── auth/
           ├── accounsts/
           ├── expenses/
        ├── components/          
        ├── styles/               
    ├── .env.local           (não incluído no repositório) 
    ├── package.json         
```

## Autenticação

A autenticação é realizada via e-mail e password, integrada ao backend Flask. Após o login, um cookie é gerado pelo backend e utilizado para identificar e autorizar o usuário nas demais páginas da aplicação.

## Validação

Por se tratar de uma aplicação simples, **não foram implementados testes automatizados** no frontend. As funcionalidades foram validadas manualmente por meio de inspeção visual, garantindo que os dados exibidos estavam de acordo com os requisitos definidos.

## Guia para execução

1. Instalar o Node.js (versão 18 ou superior)
2. Clonar o repositório
3. npm install
4. npm run dev

### Pontos de atenção
- O frontend depende do backend estar em execução e acessível via HTTPS.
- As variáveis de ambiente devem ser configuradas no arquivo .env.local

