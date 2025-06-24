# 📝 To Do List API - Flask + Oracle

Este projeto é uma API RESTful desenvolvida em **Python com Flask** que permite gerenciar **usuários** e suas respectivas **tarefas** (to-dos). O backend está conectado a um banco de dados **Oracle** e fornece endpoints para criar, atualizar, listar e deletar usuários e tarefas.

IMPORTANTE!!!!!!!!!
O projeto não está funcionando por que o banco de dados precisou ser excluido

---

## 📦 Tecnologias Utilizadas

- **Python 3.x**
- **Flask**
- **Oracle Database**
- **oracledb** (driver oficial Oracle para Python)
- **Postman** (para testes)

---

## 🔧 Instalação e Execução

### Pré-requisitos

- Python instalado (recomendado 3.9 ou superior)
- Biblioteca `oracledb` instalada

### Instalar dependências

```bash
pip install flask oracledb
```

### Executar o projeto

```bash
python app.py
```

---

## 🗄️ Estrutura do Banco de Dados

### Tabela `usuario`

| Coluna | Tipo       | Descrição               |
|--------|------------|-------------------------|
| id     | NUMBER     | Chave primária          |
| nome   | VARCHAR2   | Nome do usuário         |
| senha  | VARCHAR2   | Senha do usuário        |

### Tabela `tarefas`

| Coluna      | Tipo       | Descrição                          |
|-------------|------------|------------------------------------|
| id          | NUMBER     | Chave primária                    |
| titulo      | VARCHAR2   | Título da tarefa                   |
| descricao   | VARCHAR2   | Descrição da tarefa                |
| status      | VARCHAR2   | Status da tarefa (ex: pendente)    |
| usuario_id  | NUMBER     | ID do usuário (chave estrangeira)  |

---

## 📌 Endpoints

### 🔹 Usuários

- `GET /usuario`  
  Lista todos os usuários

- `GET /usuario/<id>`  
  Retorna um usuário por ID

- `POST /usuario`  
  Cria um novo usuário  
  ```json
  {
    "nome": "joao",
    "senha": "123"
  }
  ```

- `PUT /usuario/<id>`  
  Atualiza dados do usuário  
  ```json
  {
    "nome": "joao_atualizado",
    "senha": "nova_senha"
  }
  ```

- `DELETE /usuario`  
  Remove um usuário por ID  
  ```json
  {
    "id": 1
  }
  ```

---

### 🔹 Tarefas

- `GET /tarefas/usuario/<usuario_id>`  
  Lista todas as tarefas de um usuário

- `POST /tarefas`  
  Cria uma nova tarefa  
  ```json
  {
    "titulo": "Estudar",
    "descricao": "Estudar para a prova de Python",
    "status": "pendente",
    "usuario_id": 1
  }
  ```

- `PUT /tarefas/<id>`  
  Atualiza uma tarefa  
  ```json
  {
    "titulo": "Estudar Python",
    "status": "concluída"
  }
  ```

- `DELETE /tarefas/<id>`  
  Remove uma tarefa
