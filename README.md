# Operação Fintech Blindada – Auditoria, Correção e Hardening de uma API Financeira

Projeto desenvolvido para a disciplina **Secure Coding & Application Security**, com o objetivo de realizar a auditoria, correção e hardening de uma API financeira vulnerável, aplicando conceitos de **Secure Coding**, **OWASP Top 10 (2021)**, autenticação segura, gestão de segredos e análise estática de segurança.

---

## Objetivo do Projeto

O projeto simula um ambiente real de uma fintech (**NeoNull-Bank**) que apresentava múltiplas vulnerabilidades críticas em produção.

O objetivo foi transformar uma aplicação insegura em uma API alinhada às boas práticas de segurança sem alterar a regra de negócio original:

- Login
- Transferência financeira

---

## Vulnerabilidades Corrigidas

| Vulnerabilidade | OWASP Top 10 | Correção |
|---|---|---|
| SQL Injection | A03 – Injection | Queries parametrizadas / Prepared Statements |
| IDOR / BOLA | A01 – Broken Access Control | Controle de autorização via sessão |
| Hash MD5 | A07 – Identification and Authentication Failures | bcrypt + Salt adaptativo |
| Secret Hardcoded | Security Misconfiguration | Variáveis de ambiente (.env) |
| Debug em Produção | Security Misconfiguration | debug=False |

---

## Tecnologias Utilizadas

- Python 3
- Flask
- PostgreSQL
- SQLAlchemy
- bcrypt
- python-dotenv
- Bandit
- Safety

---

## Estrutura do Projeto

```bash
Secure Coding/
│
├── app.py
├── gerar_usuario.py
├── teste_db.py
├── requirements.txt
├── .env
│
├── evidencias/
│   ├── sqli_bloqueado.png
│   ├── idor_bloqueado.png
│   ├── bandit_scan.png
│   ├── safety_scan.png
│   └── postgres.png
│
├── relatorio/
│   ├── relatorio_operacao_fintech.pdf
│   └── relatorio_operacao_fintech_abnt.docx
│
└── README.md
```

---

## Configuração do Ambiente

### 1 Instalar dependências

```bash
pip install flask
pip install sqlalchemy
pip install psycopg2-binary
pip install bcrypt
pip install python-dotenv
pip install bandit
pip install safety
```

Ou:

```bash
pip install -r requirements.txt
```

---

## Configuração do PostgreSQL

Criar banco:

```sql
CREATE DATABASE neobank;
```

Criar tabelas:

```sql
CREATE TABLE users(

id SERIAL PRIMARY KEY,

username VARCHAR(100) UNIQUE,

password TEXT

);

CREATE TABLE contas(

id INT PRIMARY KEY,

saldo NUMERIC(10,2)

);
```

Inserir contas:

```sql
INSERT INTO contas VALUES
(1,1000),
(2,500);
```

---

## Configuração do arquivo .env

Criar arquivo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=neobank
DB_USER=postgres
DB_PASSWORD=SUA_SENHA

SECRET_KEY=NeoNullBank2026
```

---

## Gerar usuário com bcrypt

Executar:

```bash
python gerar_usuario.py
```

Inserir hash gerado:

```sql
INSERT INTO users(
username,
password
)

VALUES(

'lucas',

'$2b$12...'

);
```

---

## Executar aplicação

```bash
python app.py
```

Servidor:

```bash
http://127.0.0.1:5000
```

---

# Testes de Segurança

## Login válido

```powershell
Invoke-WebRequest `
-Uri "http://127.0.0.1:5000/login" `
-Method POST `
-Body @{

username="lucas"

password="123456"

}
```

Resultado:

```json
{"mensagem":"Login OK"}
```

---

## Teste SQL Injection

Ataque:

```sql
admin' OR '1'='1
```

Teste:

```powershell
Invoke-WebRequest `
-Uri "http://127.0.0.1:5000/login" `
-Method POST `
-Body @{

username="admin' OR '1'='1"

password="teste"

}
```

Resultado:

```json
{"erro":"Falha login"}
```

Mitigação:

✅ Prepared Statements  
✅ Query parametrizada

---

## Teste IDOR / BOLA

Teste:

```powershell
Invoke-WebRequest `
-Uri "http://127.0.0.1:5000/transferir" `
-Method POST `
-Body @{

id_origem="2"

id_destino="1"

valor="100"

}
```

Resultado:

```json
{"erro":"Operação não autorizada"}
```

Mitigação:

✅ Controle por sessão  
✅ Validação do proprietário da conta

---

# SAST – Secure Coding

Executar Bandit:

```bash
python -m bandit -r .
```

Resultado:

```text
No issues identified
```

Executar Safety:

```bash
python -m safety check
```

---

## Evidências

As evidências utilizadas no relatório encontram-se na pasta:

```bash
evidencias/
```

Arquivos:

- sqli_bloqueado.png
- idor_bloqueado.png
- bandit_scan.png
- safety_scan.png
- postgres.png

---

## Resultados Obtidos

O projeto eliminou vulnerabilidades críticas relacionadas à:

- Confidencialidade
- Integridade
- Autenticação
- Autorização
- Gestão de Segredos

A API final foi alinhada às recomendações do **OWASP Top 10 (2021)** e validada por análise SAST.

---

## Autor

**Lucas Sena**  
Engenharia da Computação  
Disciplina: Secure Coding & Application Security
