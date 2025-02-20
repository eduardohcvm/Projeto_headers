# routes/user_routes.py
from flask import render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import decode_token
from models import Usuario
from extensions import db

def get_current_user_id():
    """Recupera o ID do usuário a partir do token armazenado na sessão."""
    access_token = session.get('access_token')
    if not access_token:
        return None
    try:
        decoded = decode_token(access_token)
        return int(decoded.get("sub"))
    except Exception:
        return None

def register_user_routes(app):

    @app.route('/users', methods=['GET'])
    def users():
        """
        Lista todos os usuários.
        - Apenas admin pode ver todos os usuários.
        """
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para acessar esta página.", "error")
            return redirect(url_for('login'))

        current_user = Usuario.query.get(current_user_id)
        # Verifica se o usuário é admin
        if not (current_user and current_user.is_admin):
            flash("Você não tem permissão para ver a lista de usuários.", "error")
            return redirect(url_for('home'))

        all_users = Usuario.query.all()
        # Renderiza o template com a lista de usuários
        return render_template('user/users.html', users=all_users)

    @app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
    def edit_user(user_id):
        """
        Edita as informações de um usuário específico (nome, email, senha).
        - O próprio usuário pode se editar.
        - O admin pode editar qualquer usuário.
        """
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para editar usuários.", "error")
            return redirect(url_for('login'))

        current_user = Usuario.query.get(current_user_id)
        user = Usuario.query.get_or_404(user_id)

        # Verifica se é o próprio usuário ou se é admin
        if user.id != current_user_id and not (current_user and current_user.is_admin):
            flash("Você não tem permissão para editar este usuário.", "error")
            return redirect(url_for('users'))

        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')

            if not nome or not email or not senha:
                flash("Todos os campos são obrigatórios!", "error")
                return redirect(url_for('edit_user', user_id=user_id))

            user.nome = nome
            user.email = email
            user.senha = senha

            try:
                db.session.commit()
                flash("Usuário atualizado com sucesso!", "success")
                # Se o usuário for admin, volta para a lista; se não, volta para a home
                return redirect(url_for('users') if current_user.is_admin else url_for('home'))
            except Exception:
                db.session.rollback()
                flash("Erro ao atualizar usuário.", "error")
                return redirect(url_for('edit_user', user_id=user_id))

        # Se for GET, renderiza o formulário com dados do usuário
        return render_template('user/edit_user.html', user=user)

    @app.route('/confirm_delete_user/<int:user_id>', methods=['GET'])
    def confirm_delete_user(user_id):
        """
        Exibe a página de confirmação para exclusão do usuário.
        - O próprio usuário ou admin podem excluir.
        """
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para excluir usuários.", "error")
            return redirect(url_for('login'))

        current_user = Usuario.query.get(current_user_id)
        user = Usuario.query.get_or_404(user_id)

        # Verifica se é o próprio usuário ou se é admin
        if user.id != current_user_id and not (current_user and current_user.is_admin):
            flash("Você não tem permissão para excluir este usuário.", "error")
            return redirect(url_for('users'))

        return render_template('user/confirm_delete_user.html', user=user)

    @app.route('/delete_user/<int:user_id>', methods=['POST'])
    def delete_user(user_id):
        """
        Exclui um usuário específico.
        - O próprio usuário pode se excluir.
        - O admin pode excluir qualquer usuário.
        """
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para excluir usuários.", "error")
            return redirect(url_for('login'))

        current_user = Usuario.query.get(current_user_id)
        user = Usuario.query.get_or_404(user_id)

        # Verifica se é o próprio usuário ou se é admin
        if user.id != current_user_id and not (current_user and current_user.is_admin):
            flash("Você não tem permissão para excluir este usuário.", "error")
            return redirect(url_for('users'))

        try:
            db.session.delete(user)
            db.session.commit()
            flash("Usuário excluído com sucesso!", "success")
        except Exception:
            db.session.rollback()
            flash("Erro ao excluir usuário.", "error")

        # Se o próprio usuário se excluiu, remove o token da sessão e redireciona para login
        if user.id == current_user_id:
            session.pop('access_token', None)
            return redirect(url_for('login'))

        return redirect(url_for('users'))
