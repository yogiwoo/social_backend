from flask import Flask
from .routes.example import example_bp

def create_app():
    app=Flask(__name__)
    app.register_blueprint(example_bp)
    return app