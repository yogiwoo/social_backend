from flask import Flask
from .routes.example import example_bp
from .routes.auth import auth_bp
from .routes.posts import post_bp
from .routes.friends import friend_bp
from config import Config
from flask_jwt_extended import JWTManager
def create_app():
    app=Flask(__name__)
    app.register_blueprint(example_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(friend_bp)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY #  Change this!
    jwt = JWTManager(app)
    return app