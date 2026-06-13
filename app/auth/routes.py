from flask import Blueprint, request, jsonify

from app.auth.service import AuthService
from app.repositories.user_repository import UserRepository
from app.services.password_service import PasswordService
from app.services.jwt_service import JWTService

#  Better structure with prefix
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# =========================
# HOME ROUTE (FIX FOR 404)
# =========================
@auth_bp.route("/test", methods=["GET"])
def home():
    return jsonify({
        "message": "Auth service is running"
    })


# =========================
# REGISTER ROUTE
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = AuthService.register(data)

    return jsonify({
        "message": "User registered",
        "user_id": user.id
    })


# =========================
# LOGIN ROUTE
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = UserRepository.get_by_email(data["email"])

    if not user:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    valid = PasswordService.verify_password(
        data["password"],
        user.password_hash
    )

    if not valid:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    token = JWTService.generate_token(user.id)

    return jsonify({
        "token": token
    })