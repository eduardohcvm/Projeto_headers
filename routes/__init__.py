# routes/__init__.py
from .base_routes import register_base_routes
from .posts_routes import register_posts_routes
from .user_routes import register_user_routes

def register_routes(app):
    register_base_routes(app)
    register_posts_routes(app)
    register_user_routes(app)
