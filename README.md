
# Projeto - Rede Social em Flask

Este é um projeto de **Rede Social** desenvolvido em **Flask** que permite o cadastro e gerenciamento de **usuários** e **posts**, com controle de autenticação usando **JWT** e um CRUD completo para cada entidade.

## Funcionalidades Principais

- **Cadastro e Login de Usuários**  
- **Criação, Edição e Exclusão de Posts**  
- **Criação, Edição e Exclusão de Usuários** (incluindo lógica de admin)  
- **Controle de Acesso**  
  - Apenas usuários logados podem criar/editar/excluir posts e contas.  
  - Admin pode editar/deletar qualquer post ou usuário.  
- **Filtro de busca** para posts e usuários na página inicial.  


---

## Tecnologias Utilizadas

- **Python 3.x**
- **Flask** para construção da aplicação web
- **Flask-SQLAlchemy** para interação com o banco de dados
- **Flask-JWT-Extended** para autenticação e geração de tokens JWT
- **Docker** (opcional) para containerizar a aplicação



## Estrutura do Projeto

```
projeto/
├── app.py
├── app_config.py
├── extensions.py
├── models.py
├── run.py
├── routes/
│   ├── __init__.py
│   ├── base_routes.py
│   ├── posts_routes.py
│   └── user_routes.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── ...
└── requirements.txt
```

- **app.py**: Cria a aplicação Flask, inicializa extensões e injeta o `current_user`.
- **routes/**: Pasta que contém as rotas divididas por funcionalidade:
  - `base_routes.py`: Rotas de login, registro, home, admin, logout.
  - `posts_routes.py`: Rotas de criação, edição e exclusão de posts.
  - `user_routes.py`: Rotas para edição, listagem e exclusão de usuários.
- **templates/**: Pasta com os arquivos HTML do Flask (Jinja2).
- **requirements.txt**: Lista de dependências para instalar com `pip`.

---

## Como Rodar Localmente

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. **Criar e ativar um ambiente virtual** (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Rodar a aplicação**:
   ```bash
   python run.py
   ```
   A aplicação estará disponível em `http://127.0.0.1:5000`.

---

## Uso da Aplicação

1. **Registrar-se** em `/register` para criar um novo usuário.  
2. **Logar** em `/login` para obter acesso às funcionalidades.  
3. **Home** (`/`):  
   - Exibe lista de posts e usuários (com filtros).  
   - Botões para criar post, editar perfil etc.  
4. **Rotas de Post**:
   - **Criar**: `/create_post`
   - **Editar**: `/edit_post/<post_id>`
   - **Excluir**: `/delete_post/<post_id>`
5. **Rotas de Usuário**:
   - **Editar**: `/edit_user/<user_id>`
   - **Excluir**: `/delete_user/<user_id>`
   - **Lista de Usuários**: `/users` (apenas admin)
6. **Tornar-se Admin**: `/become_admin` (senha de admin: `12345`)

---


## Rodando com Docker (Opcional)

1. **Build da Imagem**:
   ```bash
   docker build -t nome_da_imagem .
   ```
2. **Rodar o Contêiner**:
   ```bash
   docker run -d -p 5000:5000 --name nome_do_container nome_da_imagem
   ```
3. **Acessar**:
   ```
   http://127.0.0.1:5000
   ```

---
