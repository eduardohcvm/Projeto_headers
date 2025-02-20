# app_config.py
import os

config = {
    'SQLALCHEMY_DATABASE_URI': os.getenv("DATABASE_URI", "sqlite:///crud.db"),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': os.getenv("FLASK_SECRET_KEY", "123456"),
    'JWT_SECRET_KEY': os.getenv("JWT_SECRET_KEY", "123456"),
}
