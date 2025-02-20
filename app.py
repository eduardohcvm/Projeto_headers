from flask import Flask, session
from extensions import db, jwt
from app_config import config
from flask_jwt_extended import decode_token
from models import Usuario


# Definição de um usuário anônimo para evitar erros caso autenticação de errado (não deu)
class AnonymousUser:
    is_authenticated = False
    id = None
    is_admin = False
    nome = "Convidado"


# Função para criar a aplicação
def create_app():
    # Define explicitamente o diretório de templates
    app = Flask(__name__, template_folder="templates")
    app.config.update(config)
    app.secret_key = config['SECRET_KEY']

    # Inicializa as extensões
    db.init_app(app)
    jwt.init_app(app)

    # verifica se o usuário está autenticado e injeta-o no template
    @app.context_processor
    def inject_current_user():
        access_token = session.get('access_token')
        if access_token:
            try:
                decoded = decode_token(access_token)
                user_id_str = decoded.get("sub")

                if user_id_str:
                    user = Usuario.query.get(int(user_id_str))
                    if user:
                        user.is_authenticated = True
                        return dict(current_user=user)


            except Exception as e:
                # Se o token expirou, remova-o da sessão
                if "Signature has expired" in str(e):
                    session.pop('access_token', None)
                print("Erro ao decodificar token:", e)
        return dict(current_user=AnonymousUser())

    # Registra as rotas
    with app.app_context():
        from routes import register_routes
        db.create_all()
        register_routes(app)
    return app

app = create_app()
