from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cyber_threat.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    JWTManager(app)
    db.init_app(app)

    # Auth routes
    from app.auth.routes import auth_bp
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    # Dataset routes
    from app.dataset import init_dataset
    init_dataset(app)

    # Debug: print all routes
    print("\nREGISTERED ROUTES:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app