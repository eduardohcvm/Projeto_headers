# routes/posts_routes.py
from flask import render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import decode_token
from models import Post, Usuario
from extensions import db

def get_current_user_id():
    access_token = session.get('access_token')
    if not access_token:
        return None
    try:
        decoded = decode_token(access_token)
        return int(decoded.get("sub"))
    except Exception:
        return None

def register_posts_routes(app):

    @app.route('/create_post', methods=['GET', 'POST'])
    def create_post():
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para criar posts.", "error")
            return redirect(url_for('login'))

        if request.method == 'POST':
            titulo = request.form.get('titulo')
            descricao = request.form.get('descricao')
            if not titulo or not descricao:
                flash("Título e Descrição são obrigatórios!", "error")
                return redirect(url_for('create_post'))

            post = Post(titulo=titulo, descricao=descricao, user_id=current_user_id)
            try:
                db.session.add(post)
                db.session.commit()
                flash("Post criado com sucesso!", "success")
                return redirect(url_for('home'))
            except Exception:
                db.session.rollback()
                flash("Erro ao criar post.", "error")
                return redirect(url_for('create_post'))

        return render_template('posts/create_post.html')

    @app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
    def edit_post(post_id):
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para editar posts.", "error")
            return redirect(url_for('login'))

        post = Post.query.get_or_404(post_id)
        current_user = Usuario.query.get(current_user_id)

        if post.user_id != current_user_id and not (current_user and current_user.is_admin):
            flash("Você não tem permissão para editar este post.", "error")
            return redirect(url_for('home'))

        if request.method == 'POST':
            titulo = request.form.get('titulo')
            descricao = request.form.get('descricao')
            if not titulo or not descricao:
                flash("Título e Descrição são obrigatórios!", "error")
                return redirect(url_for('edit_post', post_id=post_id))

            post.titulo = titulo
            post.descricao = descricao
            try:
                db.session.commit()
                flash("Post atualizado com sucesso!", "success")
                return redirect(url_for('home'))
            except Exception:
                db.session.rollback()
                flash("Erro ao atualizar post.", "error")
                return redirect(url_for('edit_post', post_id=post_id))

        return render_template('posts/edit_post.html', post=post)

    @app.route('/delete_post/<int:post_id>', methods=['POST'])
    def delete_post(post_id):
        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para excluir posts.", "error")
            return redirect(url_for('login'))

        post = Post.query.get_or_404(post_id)
        current_user = Usuario.query.get(current_user_id)

        if post.user_id != current_user_id and not (current_user and current_user.is_admin):
            flash("Você não tem permissão para excluir esse post.", "error")
            return redirect(url_for('home'))

        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post deletado com sucesso!", "success")
        except Exception:
            db.session.rollback()
            flash("Erro ao deletar post.", "error")

        return redirect(url_for('home'))


    @app.route('/posts/user/<int:user_id>', methods=['GET'])
    def posts_by_user(user_id):

        current_user_id = get_current_user_id()
        if not current_user_id:
            flash("Você precisa estar logado para ver posts de um usuário.", "error")
            return redirect(url_for('login'))

        user = Usuario.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id).all()
        return render_template('posts/posts_by_user.html', user=user, posts=posts)
