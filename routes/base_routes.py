# routes/base_routes.py
from flask import render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import create_access_token, decode_token
from models import Usuario, Post
from extensions import db

def register_base_routes(app):

    @app.route('/', methods=['GET'])
    def home():
        if 'access_token' not in session:
            flash("Você precisa estar logado para acessar a Home.", "error")
            return redirect(url_for('login'))

        # Filtro para buscar posts por ID
        post_id = request.args.get('post_id')
        if post_id:
            try:
                post_id_int = int(post_id)
                posts = Post.query.filter_by(id=post_id_int).all()
            except ValueError:
                posts = []
                flash("ID inválido para busca de post.", "error")
        else:
            posts = Post.query.all()

        # Filtro para buscar usuários por nome
        user_query = request.args.get('user_query')
        if user_query:
            users = Usuario.query.filter(Usuario.nome.ilike(f"%{user_query}%")).all()
        else:
            users = Usuario.query.all()

        return render_template('basic/index.html', posts=posts, users=users)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('access_token'):
            flash("Você já está logado!", "info")
            return redirect(url_for('home'))
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')
            user = Usuario.query.filter_by(email=email).first()
            if user and user.senha == senha:
                access_token = create_access_token(identity=str(user.id))
                session['access_token'] = access_token
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for('home'))
            flash("Credenciais inválidas", "error")
            return redirect(url_for('login'))
        return render_template('basic/login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if session.get('access_token'):
            flash("Você já está logado!", "info")
            return redirect(url_for('home'))
        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            if not nome or not email or not senha:
                flash("Todos os campos são obrigatórios!", "error")
                return redirect(url_for('register'))
            if Usuario.query.filter_by(email=email).first():
                flash("Email já registrado", "error")
                return redirect(url_for('register'))
            user = Usuario(nome=nome, email=email, senha=senha)
            try:
                db.session.add(user)
                db.session.commit()
                flash("Usuário registrado com sucesso!", "success")
                return redirect(url_for('login'))
            except Exception:
                db.session.rollback()
                flash("Erro ao registrar usuário.", "error")
                return redirect(url_for('register'))
        return render_template('basic/register.html')

    @app.route('/become_admin', methods=['GET', 'POST'])
    def become_admin():
        if not session.get('access_token'):
            flash("Você precisa estar logado para se tornar admin.", "error")
            return redirect(url_for('login'))
        try:
            decoded = decode_token(session['access_token'])
            user_id = int(decoded.get("sub"))
        except Exception:
            flash("Token inválido.", "error")
            return redirect(url_for('login'))
        if request.method == 'POST':
            admin_pass = request.form.get('admin_pass')
            if admin_pass == "12345":
                user = Usuario.query.get(user_id)
                user.is_admin = True
                try:
                    db.session.commit()
                    flash("Você se tornou admin!", "success")
                except Exception:
                    db.session.rollback()
                    flash("Erro ao atualizar status de admin.", "error")
                return redirect(url_for('home'))
            else:
                flash("Senha de admin incorreta.", "error")
                return redirect(url_for('become_admin'))
        return render_template('user/become_admin.html')  # <--- Subpasta user

    @app.route('/logout')
    def logout():
        session.pop('access_token', None)
        flash("Logout realizado com sucesso!", "success")
        return redirect(url_for('login'))
