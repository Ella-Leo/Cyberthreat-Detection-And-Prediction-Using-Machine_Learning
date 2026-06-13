from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.password_service import PasswordService

class AuthService:

    @staticmethod
    def register(data):

        password_hash = PasswordService.hash_password(
            data["password"]
        )

        user = User(
            fullname=data["fullname"],
            username=data["username"],
            email=data["email"],
            password_hash=password_hash,
            role_id=2
        )

        UserRepository.create(user)

        return user