from flask import Flask
from .routes.example import example_bp
from .routes.auth import auth_bp
def create_app():
    app=Flask(__name__)
    app.register_blueprint(example_bp)
    app.register_blueprint(auth_bp)
    return app