from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    # CONFIG
    app.config["JWT_SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cyber_threat.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # INIT EXTENSIONS
    JWTManager(app)
    db.init_app(app)

    # -------------------------
    # AUTH MODULE
    # -------------------------
    from app.auth.routes import auth_bp
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    # -------------------------
    # DATASET MODULE (ADD THIS)
    # -------------------------
    from app.dataset import init_dataset
    init_dataset(app)

    return app